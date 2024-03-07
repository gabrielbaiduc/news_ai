import logging
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from .scraper_utilities import fetch, parse, get_date
from config.settings import selector_configs, today

logger = logging.getLogger(__name__)


def scrape_links(section, source):
    """
    Scrape links from a section of a source.
    
    Parameters:
        section (str): The url of the section
        source (str): The source news site
    
    Returns:
        list: A list of scraped links.
    """
    content = fetch(section)
    parsed_content = parse(content)
    selectors = selector_configs[source].values()
    link_selector, link_prefix, _, _, _ = selectors
    link_elements = parsed_content.select(link_selector)
    links = [urljoin(link_prefix, link["href"]) for link in link_elements]
    logger.info(f"Scraped {len(links)} links from {section}\n")
    return links


def scrape_contents(link, source, category):
    """
    Scrape article content from a given link.
    
    Parameters:
        link (str): The link to the article.
        source (str): The source news site.
        category (str): The category of the article.
        selector_configs (dict): A dictionary of CSS selector configurations.
    
    Returns:
        dict: A dictionary containing the article's title, text content, 
              publication date, link, source, category, and word count.
    """
    content = fetch(link)
    parsed_content = parse(content)
    selectors = selector_configs[source].values()
    _, _, title_selector, text_selector, date_selector = selectors

    # Validate and scrape date
    date_element = parsed_content.select_one(date_selector)
    if date_element is None:
        return "date selector error"
    publication_date = get_date(date_element)
    if publication_date != today:
        return "out of date"

    # Validate and scrape title
    title_element = parsed_content.select_one(title_selector)
    if title_element is None:
        return "title selector error"
    title = title_element.text.strip()

    # Validate and scrape text content
    paragraph_elements = parsed_content.select(text_selector)
    if paragraph_elements is None:
        return "text selector error"
    paragraphs = [p.text.strip() for p in paragraph_elements]
    text_content = ''.join(paragraphs)

    # Get the word count of the text content
    word_count = len(text_content.split())

    return {
        "title": title,
        "text": text_content,
        "date": publication_date,
        "link": link,
        "source": source,
        "category": category,
        "word_count": word_count
    }
