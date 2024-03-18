import json
from pathlib import Path
from datetime import datetime
import logging

from utils.helpers import isoutdated

logger = logging.getLogger(__name__)


class DataManager:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent
        self.file_extension = ".json"

    def load(self, filename="articles"):
        data_path = self.base_dir / "data" / (filename + self.file_extension)
        if data_path.exists():
            try:
                with data_path.open("r") as file:
                    data = json.load(file)
                    self.datetime_converter(data, to_iso=False)
                    logger.debug(f"Loaded {data_path}")
                    return data
            except json.JSONDecodeError as error:
                logger.error(f"Decoder error while loading {data_path}: {error}")
                return None
        else:
            logger.error(f"File not found: {data_path}")
            return []

    def save(self, data, filename=None):
        if not filename:
            logger.error(f"No filename given, give a filename when saving.")
            return
        data_path = self.base_dir / "data" / (filename + self.file_extension)
        self.datetime_converter(data)
        with data_path.open("w") as file:
            json.dump(data, file, indent=4)
            logger.debug(f"Saved {data_path}")
                
    def update_current(self, current=None):
        if not current:
            current = self.load()
        discarded = self.load("discarded")
        if current and discarded:
            counter = 0
            for article in current[:]:
                if isoutdated(article["published"]):
                    discarded.append(article["url"])
                    current.remove(article)
                    counter += 1
            logger.info(f"Updated local data, {counter} articles discarded")
            self.save(current, "articles")
            self.save(discarded, "discarded")
            return current
        else:
            logger.error(f"Data files not found. Please check your data files.")

    def datetime_converter(self, data, to_iso=True):
        for article in data:
            try:
                if to_iso:
                    if isinstance(article, dict) and article["published"]:
                        article["published"] = article["published"].isoformat()
                        article["modified"] = article["modified"].isoformat()
                else:
                    if isinstance(article, dict) and article["published"]:
                        article["published"] = datetime.fromisoformat(article["published"])
                        article["modified"] = datetime.fromisoformat(article["modified"])
            except ValueError as error:
                logger.error(f"Error converting datetime for article: {error}")
            
