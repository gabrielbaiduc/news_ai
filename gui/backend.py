import logging
import asyncio
import json

from PyQt5.QtCore import QThread, pyqtSignal

from data_manager.manager import DataManager
from scraping.scrape import FetchHTML, ScrapeLinks, ScrapeContents
from summarising.summarise import Summary, PostJSON
from utils.helpers import PrepareForGUI
from config.settings import sections

# Here is the backend workhorse. This module ties the backend logic to the GUI.
# It works on a separate thread and does the article processing work in steps.
# When finished, it signals the GUI and sends a nicely organised package of
# articles that can be displayed easily.

# Setting up logging
logger = logging.getLogger(__name__)


class ArticleProcessor(QThread):
    """
    Secondary thread that handles article preprocessing tasks like
    scraping, word-processing, analytics, summary etc.
    """
    # Define signal for status updates that carry a 'str' package
    status_update = pyqtSignal(str)
    # Define signal for end of backend process that carry the prepped articles
    finished = pyqtSignal(object)


    def run(self):
        """ 
        Main method that gets executed when 'thread.start()' is called in
        `MainWindow`.  
        """
        # Starting scraping and updating status label
        self.status_update.emit("Downloading articles")
        new_articles = self.scrape()
        
        # Starting summarising and updating status label
        self.status_update.emit("Summarising articles")
        summarised_articles = self.summarise(new_articles)

        # Starting processing and updating status label
        self.status_update.emit("Processing articles")
        prepared_articles = self.prepare_articles(summarised_articles)

        # Emiting finished signal with prepared articles
        self.finished.emit(prepared_articles)


    def scrape(self):
        """ 
        Abstracts the process of scraping away from `run`. Responsible for 
        tying together the scraping process.
        1) Fetch and parse the HTML contents of URLs specified in 'sections'
        2) Scrape article links from the HTML contents of 1)
        3) Fetch and parse the HTML concents of URSs scraped in 2)
        4) Scrape article contents from the HTML contents of 3)

        `FetchHTML` class implements an asynchronous algorithm that communicates
        with the news-sites to retrieve their HTML contents and a
        synchronous parsing algorithm, used for steps 1) and 3)
        'ScrapeLinks' class scrapes link tags from parsed HTMLs, used for step
        2)
        'ScrarpeContents' class scrapes various article contents from parsed 
        HTMLs, used for step 4)

        """
        # Initialising fetch&parser separately
        fetch = FetchHTML()

        # Step 1)
        logger.debug(f"\tFetching and parsing sections \n{150*"-"}")
        section_htmls = asyncio.run(fetch.fetch(sections))
        parsed_section_htmls = fetch.parse(section_htmls)

        # Step 2)
        logger.debug(f"\tScraping sections for article links \n{150*"-"}")
        scrapelinks = ScrapeLinks()
        new_article_links = scrapelinks.scrape(parsed_section_htmls)
        # Logging result of scraping (optional)
        scrapelinks.count_newlinks(new_article_links)

        # Step 3)
        logger.debug(f"\tFetching and parsing article links \n{150*"-"}")
        scrapecontents = ScrapeContents()
        article_htmls = asyncio.run(fetch.fetch(new_article_links))
        parsed_article_htmls = fetch.parse(article_htmls)

        # Step 4)
        logger.debug(f"\tScraping article links for contents \n{150*"-"}")
        new_articles = scrapecontents.scrape(parsed_article_htmls)

        # Passing on the newly scraped articles for further processing.
        return new_articles

    def summarise(self, articles):
        """
        Abstracts the process of summarising the articles away from 'run'.
        Responsible for communicating with OpenAI and processing summaries.
        The steps are:
        1) Compose the JSON file that is submitted to OpenAI containing the 
        instructions how to summarise and article data + the api_key 
        2) Generate a `POST` request for each article summary and return 
        the response
        3) Process the response by storing the summary and meta data with the
        article

        'Summary' class composes the JSON datafile on one end, and processes
        the response from OpenAI on the other end, used in steps 1) and 3)
        'PostJSON' implements an asynchronous algorithm that communicates with
        OpenAI and bundles the response with their respective articles, used for
        step 2).
        """
        # Step 1)
        logger.debug(f"\tComposing datafiles for summaries \n{150*"-"}")
        summary = Summary(articles)
        datafiles = summary.compose_submissionfile()

        # Step 2)
        logger.debug(f"\tRequesting summaries from OpenAI \n{150*"-"}")
        post = PostJSON()
        responses = asyncio.run(post.post(datafiles))

        # Step 3)
        logger.debug(f"\tExtracting summaries from response \n{150*"-"}")
        summarised_articles = summary.process_response(responses)
        return summarised_articles


    def prepare_articles(self, articles):
        """
        Abstracts the process of preparing the articles for the GUI.

        Params:
            articles (list): the newly scraped articles as a list of dicts
        """
        # Mergind existing and new article data.
        logger.debug(f"\tMerging new articles with old articles \n{150*"-"}")
        # Loading existing data
        manager = DataManager()
        old_articles = manager.load()
        # Validating existing data
        if old_articles and not isinstance(old_articles, json.JSONDecodeError):
            logger.info(f"Combined {len(old_articles)} existing articles with "
                f"{len(articles)} new articles."
                )
            # Merging existing data with new data
            articles.extend(old_articles)
            # Saving merged data
            manager.save(articles, "articles")
        # If no existing data or data is corrupted, save new articles only
        else:
            manager.save(articles, "articles")

        # Preparing data for GUI
        logger.debug(f"\tPreparing articles for the GUI \n{150*"-"}")
        # Updating data
        manager.update_current()
        # Loading updated data
        articles = manager.load()
        # Sorting and categorising
        prepare = PrepareForGUI(articles)
        prepared_articles = prepare.prepare()

        return prepared_articles

