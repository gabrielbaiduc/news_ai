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
        logger.info(f"Fetched {url}: {response.status_code}")
        return response.content


def parse(raw_html):
    """
    Parses raw HTML content into a BeautifulSoup object and logs the parsing 
    action.
    """
    parsed_html = BeautifulSoup(raw_html, "html.parser")
    logger.info("Parsed HTML")
    return parsed_html


def get_date(date_element):
    """
    Extracts and returns a date string from a date element, 
    formatted as 'YYYY-MM-DD'. Handles absence of date.
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
