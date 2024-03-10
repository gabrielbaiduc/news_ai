import logging
from dateutil import parser
from dateutil import tz

from utils.helpers import *

logger = logging.getLogger(__name__)


def selector_error(selector, element, url):
    if element is None:
        logger.error(f"Selector error {selector} on {url}")
        return True
    return False


def parse_datetime(string):
    parsed_datetime = parser.isoparse(string)
    standardised_datetime = parsed_datetime.astimezone(tz.tzutc())
    return standardised_datetime


def flag_outdated_url(url, articles):
    articles[url] = {
        "outdated": True,
        "scraped": False,
        "in_window": False,
    }


def tolerance_limit_reached(urls, index, articles):
    logger.warning(f"Outdated tolerance limit reached {urls[index]}")
    for url in urls[index:]:
        update_outdated(url, articles)


