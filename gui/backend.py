import asyncio
import logging

from PyQt5.QtCore import QThread, pyqtSignal

from data_manager.manager import DataManager
from scraping.scrape import FetchHTML, ScrapeLinks, ScrapeContents
from summarising.summarise import Summary, PostJSON
from utils.helpers import PrepareForGUI
from config.settings import sections

logger = logging.getLogger(__name__)

class ArticleProcessor(QThread):
    """
    Article preprocessing thread that handles article preprocessing tasks like
    scraping, word-processing, analytics, summary etc.
    """
    # Define signals for status updates and when processing is finished
    status_update = pyqtSignal(str)
    finished = pyqtSignal(object)

    def run(self):
        """Main method executed when the thread starts."""
        # Notify start of scraping
        self.status_update.emit("Scraping")
        new_articles = self.scrape()
        
        # Notify start of article summarising
        self.status_update.emit("Summarising")
        summarised_articles = self.summarise(new_articles)

        # Notify start of processing
        self.status_update.emit("Processing")
        prepared_articles = self.prepare_articles(summarised_articles)

        # Emit finished signal with processed articles when done
        self.finished.emit(prepared_articles)


    def scrape(self):
        # Initialise classes for scraping and managing the resulting data
        fetch = FetchHTML()

        # Fetch & parse section content
        logger.debug(f"\tFetching and parsing sections \n{150*"-"}")
        section_htmls = asyncio.run(fetch.fetch(sections))
        parsed_section_htmls = fetch.parse(section_htmls)

        # Scrape article links from sections
        logger.debug(f"\tScraping sections for article links \n{150*"-"}")
        scrapelinks = ScrapeLinks()
        new_article_links = scrapelinks.scrape(parsed_section_htmls)
        scrapelinks._count_newlinks(new_article_links) # log only!

        # Fetch & parse articles
        logger.debug(f"\tFetching and parsing article links \n{150*"-"}")
        scrapecontents = ScrapeContents()
        article_htmls = asyncio.run(fetch.fetch(new_article_links))
        parsed_article_htmls = fetch.parse(article_htmls)

        # Scrape article contents
        logger.debug(f"\tScraping article links for contents \n{150*"-"}")
        new_articles = scrapecontents.scrape(parsed_article_htmls)

        # Save article contents by merging with existing contents
        # manager.update_current()
        # old_articles = manager.load()
        # merged_articles = manager.merge(old_articles, new_articles)
        # manager.save(merged_articles, "articles")
        return new_articles

    def summarise(self, articles):
        # Initialise classes
        logger.debug(f"\tComposing datafiles for summaries \n{150*"-"}")
        manager = DataManager()
        summary = Summary(articles)
        datafiles = summary.compose_datafile()

        # Request summaries
        logger.debug(f"\tRequesting summaries from OpenAI \n{150*"-"}")
        post = PostJSON(datafiles)
        response_files = asyncio.run(post.post())

        # Process the response
        logger.debug(f"\tExtracting summaries from response \n{150*"-"}")
        summarised_articles = summary.process_response(response_files)
        return summarised_articles


    def prepare_articles(self, articles):
        logger.debug(f"\tMerging new articles with old articles \n{150*"-"}")
        # Manage the data
        manager = DataManager()
        old_articles = manager.load()
        if old_articles:
            logger.info(f"Combined {len(old_articles)} existing articles with "
                f"{len(articles)} new articles."
                )
            articles.extend(old_articles)
            manager.save(articles, "articles")
        else:
            manager.save(articles, "articles")


        # Prepare the data
        logger.debug(f"\tPreparing articles for the GUI \n{150*"-"}")
        manager.update_current()
        articles = manager.load()
        prepare = PrepareForGUI(articles)
        prepared_articles = prepare.prepare()
        return prepared_articles

