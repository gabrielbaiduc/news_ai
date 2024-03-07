import logging
import logging.config

from scraping.main_scraper import scrape
from data_manager.manager import load_data, save_data

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
    data = load_data()
    scrape(data)
    save_data(data)