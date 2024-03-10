from datetime import datetime
from datetime import timedelta
from dateutil import tz
from collections import defaultdict
import logging


logger = logging.getLogger(__name__)


def word_count(string):
	return len(string.split())


def get_current_time():
	current = datetime.now()
	standardised_time = current.astimezone(tz.tzutc())
	return standardised_time


def outdated(published, hours):
    current = get_current_time()
    difference = current - published
    age_limit =  timedelta(hours=hours)
    if difference > age_limit:
        return True
    return False


def datetime_converter(data, to_iso=True):
	if to_iso:
	    for article in data.values():
	        if "published" in article and article["published"]:
	            article["published"] = article["published"].isoformat()
	        if "modified" in article:
	            article["modified"] = article["modified"].isoformat()
        	if "last_checked" in article:
	            article["last_checked"] = article["last_checked"].isoformat()
	else:
		for article in data.values():
			if "published" in article and article["published"]:
			    article["published"] = datetime.fromisoformat(article["published"])
			if "modified" in article:
				article["modified"] = datetime.fromisoformat(article["modified"])
			if "last_checked" in article:
				article["last_checked"] = datetime.fromisoformat(article["last_checked"])


def count_new_articles(new_articles):
    counts = defaultdict(lambda: defaultdict(int))
    for article in new_articles.values():
        if article["scraped"]:
            source = article['source']
            for category in article['category']:
                counts[source][category] += 1

    # Step 2: Log the structure using logger.info()
    for source, category_counts in counts.items():
        for cat, count in category_counts.items():
            logger.info(f'Source: {source}, Category: {cat}, Count: {count}')