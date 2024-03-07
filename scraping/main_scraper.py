import logging
import logging.config

from scraping.scrapers import scrape_links, scrape_contents
from data_manager.manager import load_data, save_data
from config.settings import (
    selector_error_messages, section_configs, ood_tolerance
)
from scraping.scraper_utilities import (
    add_article, link_visited, tolerance_limit_reached
)

logger = logging.getLogger(__name__)


def handle_links(data, links, source, category, ood_tolerance):
    """
    Handles most of the scraping work. 1) Checks if links were scraped or known 
    to be outdated. 2) Scrapes article contents if link checks pass. 3) Checks
    the contents for correct date and selector errors. 4) Stores scraped article
    if content checks pass.

    Parameters:
        data (dick): The main data structure
        links (list): List of links from section
        source (str): The source of the articles being scraped
        category (str): The category the articles belong to
        ood_tolerance (int): The number of consecutive out-of-date articles at 
        which the program discards the rest of the links in the list and breaks
        execution
        counter (int): Keeps count of scraped articles from each section
    """
    tolerance = ood_tolerance

    for index, link in enumerate(links):
        if link_visited(data, link, category):
            continue
        contents = scrape_contents(link, source, category)
        if contents == "out of date":
            tolerance -= 1
            if tolerance_limit_reached(data, link, links, index, tolerance):
                break
            continue
        if contents in selector_error_messages:
            logger.error(f"ERROR: {contents}\n")
            continue
        add_article(contents, data)
        tolerance = ood_tolerance


def handle_sections(data, source):
    """
    Scrapes the sections for article links. Each section provides a more or
    less ordered list of links to articles. More or less because some sections
    have different structure with older articles on top. 

    Parameters:
        data (dict): The main data structure
        source (str): The source of the section being scraped
    """
    for section, category in section_configs[source]:
        counter = 0
        logger.info(f"----->Scraping {section}<-----")
        links = scrape_links(section, source)
        handle_links(data, links, source, category, ood_tolerance)


def scrape(data):
    """
    The main scraping loop. Loads or initialises main data structure and 
    proceeds scraping each section for every source. Once complete, it saves the
    data.
    """
    sources= ["bbc", "nyt", "aj"]
    #data = load_data()
    for source in sources:
        logger.info(f"----->Scraping {source.upper()}<-----\n\n{200*"-"}")
        handle_sections(data, source)
    #save_data(data)