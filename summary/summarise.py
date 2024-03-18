import asyncio
import math
import logging

import aiohttp

from config.settings import *
from data_manager.manager import DataManager


logger = logging.getLogger(__name__)


class PostJSON:
    def __init__(self, datafiles, rate_limit=5):
        self.rate_limit = rate_limit
        self.datafiles = datafiles
        self.exceptions = []

    async def post(self):
        connector = aiohttp.TCPConnector(limit=self.rate_limit)
        async with aiohttp.ClientSession(headers=openai_headers, connector=connector) as session:
            tasks = [self._process_request(json, article, session) 
                     for json, article in self.datafiles]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            results = self._sort_results(results)
            logger.info(f"Posted JSON of {len(results)} articles from "
                f"{len(tasks)} concurrent tasks with "
                f"{len(self.exceptions)} exceptions"
                )
            return results

    def _sort_results(self, results):
        success = []
        for result in results:
            if isinstance(result, Exception):
                self.exceptions.append(result)
            else:
                success.append(result)
        return success

    async def _process_request(self, json, article, session):
        response_dict = await self._poster(json, session)
        return (response_dict, article)

    async def _poster(self, json, session):
        try:
            async with session.post(openai_endpoint, json=json) as response:
                response.raise_for_status()
                logger.debug(f"Requested summary {response.status}")
                return await response.json()
        except aiohttp.ClientResponseError as error:
            logger.error(f"{error.status} {error.message}")
            raise
        except aiohttp.ClientError as error:
            logger.error(f"Client error: {error} {self.url}")
            raise


class Summary:
	def __init__(self, articles):
		self.articles = articles

	def compose_datafile(self):
		datafile = []
		for article in self.articles:
			summary_count = self._calculatesummarylength(article["bodycount"])
			body = article["body"]
			system_prompt = (
				f"You will be given an article. I want you to summarise it in "
				f"'{summary_count} words'."
			)
			json = {
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
			datafile.append((json, article))
			logger.debug(f"Composed JSON file for {article["url"]}")
		logger.info(f"Composed {len(datafile)} datafiles for "
			f"{len(self.articles)} articles")
		return datafile

	def process_response(self, response_files):
		summarised_articles = []
		for response_dict, article in response_files:
			summary = response_dict["choices"][0]["message"]["content"]
			tokens_sent = response_dict["usage"]["prompt_tokens"]
			tokens_received = response_dict["usage"]["completion_tokens"]
			article["summary"] = summary
			article["tokens_sent"] = tokens_sent
			article["tokens_received"] = tokens_received
			article["summarycount"] = len(summary.split())
			article["relativesize"] = self._relative_summary_size(article)
			summarised_articles.append(article)
			logger.debug(f"Stored summary for {article["url"]}")
		logger.info(f"Summarised {len(summarised_articles)} articles from "
			f"{len(self.articles)} articles scraped")
		return summarised_articles

	# def _filter_summarised(self):
	# 	for article in self.articles:
	# 		if "summary" not in article.keys():
	# 			self.unsummarised_articles.append(article)
	# 	logger.debug(f"{len(self.unsummarised_articles)} are processed "
	# 		f"for summary."
	# 		)

	def _calculatesummarylength(self, bodycount):
		return round(40 + 65.24*math.log(0.01*bodycount))

	def _relative_summary_size(self, article):
		return round((article["summarycount"]/article["bodycount"]*100))

