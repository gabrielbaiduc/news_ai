import logging
import logging.config

from scrapers.scrapers import scrape_links, scrape_contents
from data_manager.manager import load_data, save_data
from config.settings import (
    selector_error_messages, section_configs, ood_tolerance
)
from utils.helpers import add_article, link_visited, tolerance_limit_reached


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



def handle_links(data, links, source, category, ood_tolerance):
    tolerance = ood_tolerance
    for index, link in enumerate(links):
        if link_visited(data, link, category):
            continue
        contents = scrape_contents(link, source, category)
        if contents == "out of date":
            if tolerance_limit_reached(data, link, links, index, tolerance):
                break
            continue
        if contents in selector_error_messages:
            logging.error(f"ERROR: {contents}\n")
            continue
        add_article(contents, data)
        tolerance = ood_tolerance


def handle_sections(data, source):
    for section, category in section_configs[source]:
        links = scrape_links(section, source)
        handle_links(data, links, source, category, ood_tolerance)

def main(data):
    sources= ["bbc", "nyt", "aj"]
    for source in sources:
        logging.info(f"Scraping {source.upper()}\n\n{200*"-"}")
        handle_sections(data, source)
               


if __name__ == '__main__':
    setup_logging()
    data = load_data()
    main(data)
    save_data(data)