import logging

from scraping.scrapers import *
from scraping.scraper_utilities import *
from utils.helpers import *

logger = logging.getLogger(__name__)

ood_tolerance = 4


def handle_urls(section, articles):
    urls, category, source = section
    tolerance = ood_tolerance
    for index, url in enumerate(urls):
        # LinkCheck: either stored as outdated or  under a different category
        if url in articles:
            if articles[url]["outdated"]:
                continue
            if category not in articles[url]["category"]:
                articles[url]["category"].append(category)
                logger.info(f"Category {category} added to {url}")    
                continue

        # VisitLink: scrape and validate header contents 
        header_contents = scrape_header(url)
        if not header_contents:
            continue
        published, modified, headline, description = header_contents

        # DateCheck: published more than 36h ago? flag outdated and store ...
        # for future LinkChecks
        if outdated(published, 36):
            flag_outdated_url(url, articles)
            # Tolerance: when 0, all articles left in section are outdated ...
            tolerance -= 1
            if tolerance == 0:
                # ... we break the loop and go next section
                tolerance_limit_reached(urls, index, articles)
                break
            continue

        # ScrapeBody: scrape and validate body
        body = scrape_text(url, source)
        if not body:
            continue

        # AllChecksPass: article is green, flag scraped and in_winow, store
        articles[url] = {
            "outdated": False,
            "scraped": True,
            "in_window": True,
            "published": published,
            "modified": modified,
            "last_checked": get_current_time(),
            "headline": headline,
            "description": description,
            "body": body,
            "body_count": word_count(body),
            "category": [category],
            "source": source
        }

        # Tolerance: reset for succesful scrape
        tolerance = ood_tolerance
        logger.info(f"Stored {url}")

def handle_sections(section_urls):
    # LinkList: old->new, usually first link is newest, last link is oldest ...
    # ... tolerance is for old links that are on top.
    articles = {}
    for section in section_urls:
        handle_urls(section, articles)
    return articles




def scrape(data):
    sources= ["aj", "bbc", "nyt", "ap"]
    # LinkList: get list of URLs from section, 10-50 links\section
    section_urls = scrape_urls_from_sections(sources, data)
    new_articles = handle_sections(section_urls)
    count_new_articles(new_articles)
    return new_articles
