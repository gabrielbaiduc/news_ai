import logging
import logging.config

from scraping.scrape import scrape
from data_manager.manager import *
from gui.gui import *
from summary.summarise import get_summary

def setup_logging():
    """
    Configures the logging settings for the application.
    """
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'fileHandler': {
                'class': 'logging.FileHandler',
                'filename': 'logs/scraping.log',  
                'mode': 'a',  
                'formatter': 'detailed',  
            },
        },
        'formatters': {
            'detailed': {
                'format': '%(asctime)s %(levelname)s \t\t %(message)s'
            },
        },
        'loggers': {
            '': {  
                'handlers': ['fileHandler'],
                'level': 'INFO',  
                'propagate': True, 
            },
        }
    })         
if __name__ == '__main__':
    setup_logging()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
