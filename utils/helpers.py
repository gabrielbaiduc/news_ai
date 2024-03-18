from datetime import datetime
from datetime import timedelta
from dateutil import tz
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


def get_current_time():
	current = datetime.now()
	standardised_time = current.astimezone(tz.tzutc())
	return standardised_time


def isoutdated(published, hours=24):
    current = get_current_time()
    difference = current - published
    age_limit =  timedelta(hours=hours)
    if difference > age_limit:
        return True
    return False

class PrepareForGUI:
    def __init__(self, articles):
        self.articles = articles

    def prepare(self):
        sortd = self._sort()
        categorised = self._categorise(sortd)
        logger.info(f"Prepared {len(sortd)} articles for the GUI.")
        return categorised

    def _sort(self):
        sortebypubdate = sorted(
            self.articles, 
            key=lambda x: x["published"], 
            reverse=True)
        return sortebypubdate

    def _categorise(self, articles):
        category_list = {}
        for article in articles:
            for category in article["category"]:
                if category not in category_list:
                    category_list[category] = []
                category_list[category].append(article)
        return category_list





