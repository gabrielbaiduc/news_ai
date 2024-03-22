import logging
import asyncio
import json

from PyQt5.QtCore import QThread, pyqtSignal

from data_manager.manager import DataManager
from scraping.scrape import FetchHTML, ScrapeLinks, ScrapeContents
from summarising.summarise import Summary, PostJSON, Merge
from grouping.preprocess import Preprocess
from grouping.group import Group
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
        if not new_articles:
            self.status_update.emit("Processing articles")
            prepared_articles = self.prepare_articles()
            self.finished.emit(prepared_articles)
        
        else:
            # Starting summarising and updating status label
            self.status_update.emit("Summarising articles")
            summarised_articles = self.summarise(new_articles)

            # Preprocessing
            self.status_update.emit("Preprocessing articles")
            preprocessed_articles = self.preprocess(summarised_articles)

            # Grouping text
            self.status_update.emit("Grouping articles")
            self.group()

            # Starting processing and updating status label
            self.status_update.emit("Processing articles")
            prepared_articles = self.prepare_articles()

            # Emiting finished signal with prepared articles
            self.finished.emit(prepared_articles)


    def scrape(self):
        """ 
            Abstracts the process of scraping away from `run`. Responsible for 
            tying together the scraping process. Returns a list of newly scraped
            articles.
        """
        # Initialising requests
        fetch = FetchHTML()

        # Fetching HTMLs from sections
        section_htmls = asyncio.run(fetch.fetch(sections))
        parsed_section_htmls = fetch.parse(section_htmls)

        # Scraping links from section HTMLs
        scrapelinks = ScrapeLinks()
        new_article_links = scrapelinks.scrape(parsed_section_htmls)
        # Logging result of scraping (optional)
        scrapelinks.count_newlinks(new_article_links)

        # Fetching article HTMLs
        article_htmls = asyncio.run(fetch.fetch(new_article_links))
        parsed_article_htmls = fetch.parse(article_htmls)

        # Scraping article contents
        scrapecontents = ScrapeContents()
        new_articles = scrapecontents.scrape(parsed_article_htmls)

        return new_articles

    def summarise(self, articles):
        """
            Abstracts the process of summarising the articles away from 'run'.
            Returns summarised articles.
        """
        # Composing submission files
        summary = Summary(articles)
        submissionfiles = summary.compose_submissionfile()

        # Requesting summaries
        post = PostJSON()
        responses = asyncio.run(post.post(submissionfiles))

        # Processing responses
        summarised_articles = summary.process_response(responses)

        return summarised_articles


    def preprocess(self, summarised_articles):
        """ 
            Abstracts the preprocessing away from 'run'.
        """
        # Preprocessing article's text contents
        preprocessor = Preprocess()
        preprocessed_articles = preprocessor.process(summarised_articles)

        # Merging old articles with new ones and saving merged
        manager = DataManager()
        old_articles = manager.load()
        if old_articles and not isinstance(old_articles, json.JSONDecodeError):
            logger.info(f"Combined {len(old_articles)} existing articles with "
                f"{len(preprocessed_articles)} new articles."
                )
            preprocessed_articles.extend(old_articles)
            manager.save(preprocessed_articles, "articles")

        # logging corrupted file
        elif isinstance(old_articles, json.JSONDecodeError):
            logger.error(f"'articles.json' is corrupt. Could not save")

        # Saving new articles only, likely on first run
        else:
            logger.warning(f"No data found when trying to merge new with old")
            manager.save(preprocessed_articles, "articles")


    def group(self):
        """
            Abstracts the process of grouping away from 'run'. Handles the 
            clustering of articles and the subsequent merging of summaries
            via OpenAI.
        """
        # Grouping articles
        grouper = Group()
        grouper.group()

        # Merging summaries of groups
        merger = Merge()
        merger.merge()



    def prepare_articles(self):
        """
        Abstracts the process of preparing the articles for the GUI.
        """
        # Updating data
        manager = DataManager()
        manager.update_current()

        # Sorting and categorising
        prepare = PrepareForGUI()
        prepared_articles = prepare.prepare()

        return prepared_articles

