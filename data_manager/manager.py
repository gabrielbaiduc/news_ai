import json
from pathlib import Path
from datetime import datetime
import logging

# DataManager module responsible for operations on locally stored data
# ToDo:
# 1) streamline 'DataManager', review how and where it's used, reduce the number
#   of unnecessary load and save operations (like in 'update_current'). 
#   main use is in 'gui/backend.py' so rewrite the thread class to handle data
#   management better.
# 2) fix circular import with 'utils/helpers.py' using 'isoutdated'
logger = logging.getLogger(__name__)


class DataManager:
    """ 
    Data manager class that is responsible for handling loading, saving, merging
    updating operations on data saved locally. 

    `articles.json` - the main file for current articles that are ready for 
    display. A list of dictionaries, each dictionary is a fully 
    processed article with keys: 
    - 'url' (str)
    - 'published' (str in file, datetime when loaded)
    - 'modified' (same as 'published')
    - 'bodycount' (int, word count of the body)
    - 'source' (str, read more in 'config/settings.py')
    - 'category' (str, read more in 'config/settings.py')
    - 'headline' (str)
    - 'descirption' (str)
    - 'body' (str)
    - 'summary' (str)
    - 'tokens_sent' (int, the token cost of the body)
    - 'tokens_received' (int, the coken cost of the summary)
    - 'summarycount' (int, word count of the summary)
    - 'relativesize' (int, size of summary relative to body in %)

    'discarded.json' - a list of URLs that were procesed and discraded before,
    could be outdated or failed some check during scraping. 

    'archive.json' - a list of scraped articles that I archived. I'm planning to
    use these + 'articles.json' to train clustering models that group articles.
    """
    def __init__(self):
        """ Initialise data storage location and format """
        self.base_dir = Path(__file__).resolve().parent.parent
        self.file_extension = ".json"


    def load(self, filename="articles"):
        """ 
        Handles the loading of data from disc.

        Params:
            filename (str): the name of the file to load, w/o extension
        Returns:
            data (list) or None:
        """
        # Composing absolute path of file to load
        data_path = self.base_dir / "data" / (filename + self.file_extension)

        # Validating absolute path
        if data_path.exists():
            try:
                # Loading data
                with data_path.open("r") as file:
                    data = json.load(file)
                    # Converting date fields from 'str' to 'datetime' object
                    self.datetime_converter(data, to_iso=False)
                    logger.debug(f"Loaded {data_path}")
                    return data
            except json.JSONDecodeError as error:
                # Logging decoder error
                logger.error(f"Decoder error while loading {data_path}: {error}")
                return None
        else:
            # Logging absolute path error
            logger.error(f"File not found: {data_path}")
            return []


    def save(self, data, filename=None):
        """
        Handles the saving of data to disc. Filename must be specified.

        Params:
            data (list): data to be saved
            filename (str): name of the file, conventionally; "articles" or
                            "discarded" (potentially "archived")
        """
        # Checking for filename
        if filename not in ["articles", "discarded", "archived"]:
            logger.error(f"No filename, or incorrect filename.")
            return

        # Compose absolute path
        data_path = self.base_dir / "data" / (filename + self.file_extension)

        # Converting date related fields from 'str' to 'datetime' object.
        self.datetime_converter(data)

        # Saving data
        with data_path.open("w") as file:
            json.dump(data, file, indent=4)
            logger.debug(f"Saved {data_path}")
                

    def update_current(self):
        """ 
        Moves outdated articles from 'articles.json' to 'discarded.json'

        """
        # Loading data
        from utils.helpers import isoutdated
        articles = self.load("articles")
        discarded = self.load("discarded")
        archived = self.load("archived")

        # Validating data by checking if 
        if all(
            not isinstance(data, json.JSONDecodeError) 
            for data in [articles, discarded, archived]
            ):

            # Initialising counter
            counter = 0
            # Updating data
            for article in articles[:]:
                if isoutdated(article["published"]):
                    discarded.append(article["url"])
                    archived.append(article)
                    articles.remove(article)
                    counter += 1

            # Logging results of update
            logger.info(f"Updated local data, {counter} articles discarded")

            # Saving data files
            self.save(articles, "articles")
            self.save(discarded, "discarded")
            self.save(archived, "archived")

        # Logging c
        else:
            logger.error(f"Data files corrupted. Please check your data files.")


    def datetime_converter(self, data, to_iso=True):
        """
        Handles datetime conversion between 'str' and 'datetime' ojbect. The
        conversion is 'in place'

        Params:
            data (list): list of articles dicts
            to_iso (bool): states the conversion directions
        """
        # Converting. Checks are in place to filter elements in the list that 
        # are not dictionaries or havent the date related field.
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
            
