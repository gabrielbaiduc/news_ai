import json
from pathlib import Path
import logging

from utils.helpers import *

logger = logging.getLogger(__name__)

base_dir = Path(__file__).resolve().parent.parent
filename = f"current_data.json"
data_path = base_dir / "data" / filename


def load_data():
    if data_path.exists():
        try:
            with data_path.open('r') as file:
                data = json.load(file)
                datetime_converter(data, to_iso=False)
                logger.info(f"Loaded from {filename}")
                return data
        except json.JSONDecodeError as err:
            logger.error(f"Decoder error while loading {filename}: {err}")
            return None
    else:
        logger.warning(f"Data doesn't exist under {filename}")
        return None


def save_data(data):
    datetime_converter(data)
    with data_path.open('w') as file:
        json.dump(data, file, indent=4)
        logger.info(f"Saved to {filename}")


def merge_data(old, new):
    if old:
        old.update(new)
        return old
    else:
        return new

def update_outdated():
    articles = load_data()
    counter = 0
    for url, article in articles.items():
        if not article["outdated"] and isoutdated(article["published"], 24):
            article["outdated"] = True
            counter += 1
    logger.info(f"Articles processed, {counter} articles were flagged as outdated")
    save_data(articles)
