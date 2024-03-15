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


def isoutdated(published, hours):
    current = get_current_time()
    difference = current - published
    age_limit =  timedelta(hours=hours)
    if difference > age_limit:
        return True
    return False


def datetime_converter(data, to_iso=True):
    for article in data.values():
        try:
            if to_iso:
                if "published" in article and article["published"]:
                    article["published"] = article["published"].isoformat()
                if "modified" in article:
                    article["modified"] = article["modified"].isoformat()
                if "last_checked" in article:
                    article["last_checked"] = article["last_checked"].isoformat()
            else:
                if "published" in article and article["published"]:
                    article["published"] = datetime.fromisoformat(article["published"])
                if "modified" in article:
                    article["modified"] = datetime.fromisoformat(article["modified"])
                if "last_checked" in article:
                    article["last_checked"] = datetime.fromisoformat(article["last_checked"])
        except ValueError as e:
            logger.error(f"Error converting datetime for article: {e}")

def count_new_articles(new_articles):
    counts = defaultdict(lambda: defaultdict(int))
    total = 0
    for article in new_articles.values():
        if not article["outdated"]:
            source = article["source"]
            for category in article["category"]:
                counts[source][category] += 1
                total += 1

    # Log the structure using logger.info()
    for source, category_counts in counts.items():
        for cat, count in category_counts.items():
            logger.info(f"Source: {source}, Category: {cat}, Count: {count}")
    logger.info(f"Total: {total}")


def isinwindow(articles):
    in_window = {}
    for url, content in articles.items():
        if not content["outdated"]:
            in_window[url] = content
    return in_window


def get_uniquecategories(articles):
    categories = []
    for url, article in articles:
        if article["scraped"]:
            for cat in article["category"]:
                if cat not in categories:
                    categories.append(cat)
    return categories


def categorise(articles):
    categorised = {cat: [] for cat in get_uniquecategories(articles)}
    for url, content in articles:
        for category in content["category"]:
            categorised[category].append((url, content["headline"], 
                content["summary"], content["source"]))
    return categorised


def process_articles():
    from data_manager.manager import load_data
    articles = load_data()
    inwindow = isinwindow(articles)
    sortedbydate = sorted(inwindow.items(), key=lambda x: x[1]["published"])
    categorised = categorise(sortedbydate)
    return categorised