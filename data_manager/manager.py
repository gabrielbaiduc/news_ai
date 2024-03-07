import json
from datetime import datetime
from pathlib import Path
import logging

from config.settings import data_keys

logger = logging.getLogger(__name__)

base_dir = Path(__file__).resolve().parent.parent
today = datetime.now().date().isoformat()
filename = f"{today}.json"
data_path = base_dir / "data" / filename


def create_empty_data_structure():
    """Create empty datastructure"""
    data = {}
    for key in data_keys:
        data[key] = []
    return data


def load_data():
    """Load data from a JSON file for today's date if it exists."""
    if data_path.exists():
        try:
            with data_path.open('r') as file:
                data = json.load(file)
                logger.info(f"{filename} loaded\n\n")
                return data
        except json.JSONDecodeError:
            logger.error("Failed to decode JSON data.\n\n")
            return create_empty_data_structure()
    else:
        logger.info(f"Data not found, creating new data structure\n\n")
        return create_empty_data_structure()


def save_data(data):
    """Save given data to a JSON file for today's date."""
    # today = datetime.now().date().isoformat()
    # data_path = BASE_DIR / 'data' / f'{today}.json'
    # data = {}
    # for data_dict in kwargs.values():
    #     data.update(data_dict)
    with data_path.open('w') as file:
        json.dump(data, file, indent=4)
        logger.info(f"{filename} saved\n\n\n{200*"-"}\n{200*"-"}")



