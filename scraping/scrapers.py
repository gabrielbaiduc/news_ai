import logging
from urllib.parse import urljoin
import json

from bs4 import BeautifulSoup

from config.settings import selector_configs, section_configs
from utils.web_operations import fetch, parse
from scraping.scraper_utilities import selector_error, parse_datetime
from utils.helpers import word_count

logger = logging.getLogger(__name__)


def scrape_urls_from_sections(sources, data):
    section_urls = []
    for source in sources:
        for section_url, category in section_configs[source]:
            # Network
            response = fetch(section_url)
            if not response:
                continue
            soup = parse(response)

            # Selector
            selectors = selector_configs[source].values()
            selector, prefix, _ = selectors
            elements = soup.select(selector)
            if selector_error(selector, elements, section_url):
                continue

            # Scrape & validate
            hrefs = [element["href"] for element in elements]
            if source == "nyt": # EXTRA: nyt only to filter out non-text URLs.
                hrefs = [
                href for href in hrefs 
                if not href.startswith("/interactive") 
                and not href.startswith("/video")
                ]
            urls = [urljoin(prefix, href) for href in hrefs]
            if data:
                urls = [url for url in urls if url not in data]
            logger.info(f"Scraped {len(urls)} URLs from {section_url}")
            section_urls.append((urls, category, source))
    return section_urls


def scrape_header(url):
    # Network
    response = fetch(url)
    if not response:
        return None
    soup = parse(response)

    # Selector
    selector = selector_configs["ld_json"]
    element = soup.select_one(selector)
    if selector_error(selector, element, url):
        return None

    # Scrape & validate
    string = element.get_text()
    ld_json = json.loads(string)
    if isinstance(ld_json, list):
        ld_json = ld_json[0]
    if not isinstance(ld_json, dict):
        logger.error(f"Unexpected header format {url}")
        return None
    try:
        published = ld_json["datePublished"]
        modified = ld_json["dateModified"]
        headline = ld_json["headline"]
        description = ld_json["description"]
    except KeyError as err:
        logger.error(f"Missing key: {err} {url}")
        return None
    published = parse_datetime(published)
    modified = parse_datetime(modified)
    return published, modified, headline, description


def scrape_text(url, source):
    # Network
    response = fetch(url)
    if not response:
        return None
    soup = parse(response)

    # Selector
    selector = selector_configs[source]["text_selector"]
    elements = soup.select(selector)
    if selector_error(selector, elements, url):
        return None

    # Srape & validate
    ps = [element.text.strip() for element in elements]
    paragraphs = [p for p in ps if word_count(p) > 0]
    text_content = ''.join(paragraphs)
    if word_count(text_content) < 100:
        logger.info(f"Body too short {url}")
        return None
    return text_content
