import logging
import random
import requests
from bs4 import BeautifulSoup
from dateutil import parser
from requests.exceptions import HTTPError, Timeout, ConnectionError

from config.settings import user_agents

logger = logging.getLogger(__name__)


def get_random_user_agent():
    """Returns a random user agent string from the predefined list."""
    return random.choice(user_agents)


session = requests.Session()


def fetch(url):
    """
    Fetches the content of a URL using a random user agent. Logs and handles 
    possible exceptions.

    Parameters:
        url (str): The url to be fetched

    Returns:
        raw HTML content OR None if exception is raised
    """
    try:
        headers = {'User-Agent': get_random_user_agent()}
        session.headers.update(headers)
        response = session.get(url)
        response.raise_for_status()
    except HTTPError as http_err:
        logger.error(f"HTTP error occurred while fetching {url}: {http_err}")
        return None
    except ConnectionError as conn_err:
        logger.error(f"Connection error occurred while fetching {url}: {conn_err}")
        return None
    except Timeout as timeout_err:
        logger.error(f"Timeout error occurred while fetching {url}: {timeout_err}")
        return None
    except Exception as err:
        logger.error(f"An unexpected error occurred while fetching {url}: {err}")
        return None
    else:
        logger.info(f"Status: {response.status_code}, fetched {url}")
        return response.content


def parse(response_content):
    """
    Parses raw HTML content into a BeautifulSoup object and logs the parsing 
    action.

    Parameters:
        response_content (object): Raw HTML content 

    Returns:
        parsed HTML content
    """
    parsed_content = BeautifulSoup(response_content, "html.parser")
    logger.info("Parsed HTML")
    return parsed_content


def get_date(date_element):
    """
    Extracts and returns a date string from a date element, 
    formatted as 'YYYY-MM-DD'. Handles absence of date.

    Parameters:
        date_element (str): HTML element containg the date

    Returns:
        date (str): OR None OR (str): error message
    """
    if date_element and date_element.name == 'time':
        datetime_str = date_element['datetime']
    else:
        datetime_str = date_element.get_text() if date_element else None

    if datetime_str:
        try:
            parsed_date = parser.parse(datetime_str)
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            logger.error(f"Date parsing error for date string: {datetime_str}")
            return "Invalid date format"
    else:
        return "Date not found"

def add_article(article, data):
    """
    Appends article information to the corresponding keys in the data dict.

    Parameters:
        article (dict): The article contents, keys correspond with 
        main data structure
        data (dict): The main data structure
    """
    for key in article:
        if key in data:
            data[key].append(article[key])

    logger.info(f"Succesfuly scraped '{article["link"]}'\n")


def get_index(data, link):
    """
    Get the index of the article in data that matches the link.

    Parameters:
        data (dict): The main data structure
        link (str): The article's URL.
    Return:
        (int): the index 
    """
    return data["link"].index(link)


def link_visited(data, link, category):
    """
    Checks if a link has been scraped or is known to be outdated.
    If already scraped; compares the current category to the category of the
    scraped article and adds the current category if they don't match.

    Parameters:
        data (dict): The main data structure.
        link (str): The articles URL.
        category (str): The category the article belongs to.
    Returns:
        (bool) True if link is visited/outdated, False otherwise.
    """
    if link in data["link"]:
        index = get_index(data, link)
        cat = data["category"][index]
        if category not in cat:
            logger.debug(f"Existing: under {cat}, added {category} {link}\n")            
            data["category"][index] += f" {category}"
        logger.debug(f"Existing: under {cat} {link}\n")
        return True
    if link in data["outdated_links"]:
        logger.debug(f"OOD: from memory {link}\n")
        return True
    return False


def tolerance_limit_reached(data, link, links, index, tolerance):
    """
    Checks if the tolearnce-limit on out-dated-articles in a list of links from
    a section is reached.

    Parameters:
        data (dict): The main data structure
        link (str): The URL of the article currently scraped
        links (list): The list of articles scraped from the current section
        index (int): The index of `link` in `links`
        tolerance (int): The number of consecutive out-of-date articles allowed
    """
    if tolerance == 0:
        data["outdated_links"] += links[index:]
        logging.warning(f"OOD: tolerance limit reached {link}\n")
        return True
    data["outdated_links"].append(link)
    logging.warning(f"OOD: {tolerance} after {link}\n")
    return False

