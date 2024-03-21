import asyncio
import math
import logging

import aiohttp
import keyring

from config.settings import *
from data_manager.manager import DataManager


# Modules to summarise articles. It implements 2 classes, one to handle the 
# network operations and one to handle the related submissionfile operations. 


# ToDo:
# 1) Move 'PostJSON' into 'utils/http_requests.py' and combine with 'FetchHTML'

logger = logging.getLogger(__name__)

# OpenAI endpoing and model 
openai_endpoint = "https://api.openai.com/v1/chat/completions"
gpt_model = "gpt-3.5-turbo-0125"


class PostJSON:
    """ 
    Class responsible for making 'POST' requests to the OpenAI API. It compiles
    a list of tasks from submissionfile composed by `Summary` and executes them 
    concurrently. The response of each request is packaged with it's 
    corresponding article. Exceptions are re-raised up the call stack and stored
    separately. 

    Attributes:
        rate_limit (int): the rate limit
        exceptions (list): list of exceptions raised.
     """
    def __init__(self, rate_limit=5):
        """ 
        Initialise rate-limit the required submissionfile and an empty 
        exceptions list.
        
        Params:
            rate_limit (int): default is 5, with 10 the rate-limit is exceded.
        """
        self.rate_limit = rate_limit
        self.exceptions = []


    async def post(self, requests):
        """
        Main method that handles asynchronous HTTP 'POST' requests with OpenAI 
        by creating a list of tasks that can run concurrently. 

        Params:
            requests (list): list of 2-tuples (submissionfile, article)
        Returns:
            results (list): list of 2-tuples (responsefile, article_dict)
        """
        # Initialising TCP connector for rate limiting.
        connector = aiohttp.TCPConnector(limit=self.rate_limit)

        # Openin network session
        async with aiohttp.ClientSession(
                # Creating persisent header with auth. key
                headers=self._headers(), 
                connector=connector
                ) as session:

            # Creating a list of tasks
            tasks = [self._process_request(submissionfile, article, session) 
                     for submissionfile, article in requests]

            # Executing list of tasks concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Sorting good responses from bad
            results = self._sort_results(results)

            # Logging results
            logger.info(f"Posted JSON of {len(results)} articles from "
                f"{len(tasks)} concurrent tasks with "
                f"{len(self.exceptions)} exceptions"
                )

            return results


    def _sort_results(self, results):
        """
        Handles the separation of bad from good responses

        Params:
            results (list): list of 2-tuples [(responsefile, article_dict),...]
        Returns:
            success (list): list of successful 2-tuples, same as `results`
        """

        # Initialising good response container
        success = []

        # Sorting bad from good responses
        for result in results:
            if isinstance(result, Exception):
                self.exceptions.append(result)
            else:
                success.append(result)

        # Returning good results
        return success


    async def _process_request(self, submissionfile, article, session):
        """
        Async utility function that unpacks the 2-tuples as they are sent to 
        OpenAI and repacks the 2-tuples as the responses come back.

        Params:
            submissionfile (dict): dictionary containing data for OpenAI
            article (dict): article dictionary
            session (obj): session object
        Returns:
            2-tuple (tuple): response dict and corresponding article dict
        """
        # Making request
        responsefile = await self._poster(submissionfile, session)

        # Returning response package
        return (responsefile, article)


    async def _poster(self, submissionfile, session):
        """ 
        Async HTTP request function, here we make the request to OpenAI. It
        re-raises exceptions up the chain.

        Params:
            submissionfile (dict): submissionfile
            session (obj): the session object.
        """

        # Attempting request
        try:
            async with session.post(
                openai_endpoint, 
                json=submissionfile
                ) as response:
                response.raise_for_status()
                logger.debug(f"Requested summary {response.status}")
                # Returning response dict
                return await response.json()

        # Re-raising exceptions
        except aiohttp.ClientResponseError as error:
            logger.error(f"{error.status} {error.message}")
            raise
        except aiohttp.ClientError as error:
            logger.error(f"Client error: {error} {self.url}")
            raise


    def _headers(self):
        """
        Handles the secure retrieval of the auth key and composin the header 
        """

        # Retrieving auth. key
        api_key = keyring.get_password("News-AI", "openai_api_key")

        # Composing header with auth. key
        headers = {"Authorization": f"Bearer {api_key}"}

        return headers


class Summary:
    """
    Class responsible for  the composition and packagin of the required 
    submissionfile to communicate with the OpenAI API and the processing of the 
    responses.
    """
    def __init__(self, articles):
        """
        Initialise list of articles to summarise.

        Params:
            articles (list): list of article dicts
        """
        self.articles = articles


    def compose_submissionfile(self):
        """
        Handles the composition of the submissionfile sent to OpenAI

        Returns:
            submissions (tuple): 2-tuple containing the submissionfile and article 
            dicts
        """

        # Initialising empty submissions container
        submissions = []

        # Iterating over articles 
        for article in self.articles:
            # Calculating desired summary length
            summary_count = self._calculatesummarylength(article["bodycount"])
            # Composing system prompt
            system_prompt = (
                f"You will be given an article. I want you to summarise it in "
                f"'{summary_count} words'."
            )
            # Extracting body of article
            body = article["body"]
            # Composing submissionfile
            submissionfile = {
                    "model": gpt_model,
                    "messages": [{
                        "role": "system",
                        "content": system_prompt
                    },{
                        "role": "user",
                        "content": body
                }],
                "temperature": 0.5,
                "max_tokens": 1000,
                "top_p": 1.0,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.0
            }
            # Adding completed submissionfile along with the article to the list 
            # of submissions
            submissions.append((submissionfile, article))
            logger.debug(f"Composed JSON file for {article["url"]}")

        # Logging results
        logger.info(f"Composed {len(submissions)} submissionfile for "
            f"{len(self.articles)} articles")

        return submissions


    def process_response(self, results):
        """
        Handles the processing of the response file received from OpenAI
        by extracting the summary and other metadata and adding them to the
        corresponding article dictionary

        Params:
            results (list): list of 2-tuples [(responsefile, article_dict),...]
        Returns:
            summarised_articles (list): list of article dicts with summaries
        """
        # Initialising empty article container
        summarised_articles = []

        # Iterating over tuples in `results`
        for responsefile, article in results:
            # Extracting summary, tokens received and sent
            summary = responsefile["choices"][0]["message"]["content"]
            tokens_sent = responsefile["usage"]["prompt_tokens"]
            tokens_received = responsefile["usage"]["completion_tokens"]
            # Adding summary and tokens fields to article dict
            article["summary"] = summary
            article["tokens_sent"] = tokens_sent
            article["tokens_received"] = tokens_received
            # Calculating lenght of summary and adding it to article dict
            article["summarycount"] = len(summary.split())
            # Calculating size of summary relative to original in % and adding
            # it to article dict
            article["relativesize"] = self._relative_summary_size(article)
            # Storing extended article dict
            summarised_articles.append(article)
            logger.debug(f"Stored summary for {article["url"]}")

        # Logging result of processing the responses
        logger.info(f"Summarised {len(summarised_articles)} articles from "
            f"{len(self.articles)} articles scraped")

        return summarised_articles


    def _calculatesummarylength(self, bodycount):
        """
        A logistic equation I formulated to calculate the desired lenght of the
        summary based on the lenght of the original. The summary lenght is 
        proportional to the original's lenght, with 100 word-long articles 
        getting summaries of 40% of the original's lenght and articles longer
        than 2000 words getting summaries of 10% of the originals lenght. The 
        curve of the function travels between the two and decreases fast 
        initially and slows down for longer articles. This tackles 2 problems
        1) the summaries are kept around the same lenght 
        2) shorter articles need longer relative summaries otherwise ChatGTP
            produces very terse summaries. Read more about this on my blog.
        """
        return round(40 + 65.24*math.log(0.01*bodycount))


    def _relative_summary_size(self, article):
        """
        Calculates the length of the summary relative to the lenght of the 
        articles.
        """
        return round((article["summarycount"]/article["bodycount"]*100))

