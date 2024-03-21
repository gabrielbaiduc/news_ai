import logging
from datetime import datetime
from datetime import timedelta
from collections import defaultdict

from dateutil import tz

# Holds auxileary classe and functions that work with data or perform checks 
# on data. For the most part, these are here because I didn't know where else to
# put them

# ToDo:
# 1) Create a time related class that implements `get_current_time` and 
#   `isoutdated`.

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
    """ 
    Utility class that organises articles so it's easier for the GUI to display
    """
    def __init__(self, articles):
        """ 
        Initialise articles to prepare. 
        
        Attr:
            articles (list): a list of articles where each article is a dict
        """
        self.articles = articles


    def prepare(self):
        """ 
        The main method that prepares the articles.

        Returns:
            prepared (dict): dictionary with categories as keys and a list of
                                articles belonging to that category as values
        """
        # Sorting
        sortd = self._sort()

        # Categorising
        prepared = self._categorise(sortd)

        # Logging results
        logger.info(f"Prepared (sorted and categorised) {len(sortd)} articles " 
                    f"for the GUI.")

        return prepared


    def _sort(self):
        """ 
        Handles sorting the list of articles. Sorting order is newest first. 
        
        Returns:
            sortedbypubdate (list): list of sorted articles
        """
        # Sorting by date published
        sortebypubdate = sorted(
            self.articles, 
            key=lambda x: x["published"], 
            reverse=True)

        return sortebypubdate

    def _categorise(self, articles):
        """
        Handles the categorisation of articles by creating a dictionary with
        the avaiable categories as keys and lists of corresponding articles.
        Articles that belong to multiple categories are placed in all of the
        categories. This ensures that the GUI can iterate over the categories
        then create and populate the tab with the articles.
        """
        # Initialising holding dict
        categorised = {}

        # Categorising
        for article in articles:
            for category in article["category"]:
                if category not in categorised:
                    categorised[category] = []
                categorised[category].append(article)

        return categorised





