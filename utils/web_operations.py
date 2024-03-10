import logging
import random
import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError, Timeout, ConnectionError

from config.settings import api_key

# Requests session and random user agents, used to avoid 403 when fetching html content
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/86.0.4240.93 Mobile/15E148 Safari/604.1',
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.57",
    "Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (X11; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36 OPR/49.0.2725.64"
]

# Contains Authorizatin key
openai_header = {"Authorization": f"Bearer {api_key}"}

logger = logging.getLogger(__name__)

session = requests.Session()


def get_random_user_agent():
    return random.choice(user_agents)


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
        logger.debug(f"Fetched {url}: {response.status_code}")
    return response


def parse(response):
    """
    Parses raw HTML content into a BeautifulSoup object and logs the parsing 
    action.

    Parameters:
        response_content (object): Raw HTML content 

    Returns:
        parsed HTML content
    """
    response_content = response.content
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


def post(data):
    # required content for OpenAI API post request
    url = "https://api.openai.com/v1/chat/completions"

    try:
        response = session.post(url, headers=openai_header, json=data)
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
        logger.info(f"Status: {response.status_code} - {url}")

    return response