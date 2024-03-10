import logging
import logging.config

from scraping.scrape import scrape
from data_manager.manager import load_data, save_data, merge_data


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
    articles = load_data()
    new_articles = scrape(articles)
    merged_data = merge_data(articles, new_articles)
    save_data(merged_data)