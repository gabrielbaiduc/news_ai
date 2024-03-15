from PyQt5.QtCore import QThread, pyqtSignal

from scraping.scrape import scrape
from data_manager.manager import *
from utils.helpers import *
from summary.summarise import get_summary

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
        scrape()
        
        # Notify start of article summarising
        self.status_update.emit("Summarising")
        update_outdated()
        get_summary()

        # Notify start of processing
        self.status_update.emit("Processing")
        processed_articles = process_articles()

        # Emit finished signal with processed articles when done
        self.finished.emit(processed_articles)