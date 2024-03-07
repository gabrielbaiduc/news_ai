import logging

logger = logging.getLogger(__name__)



def add_article(article, data):
    """
    Appends article information to the corresponding keys in the data dict.

    :param article: Dict containing article contents.
    :param data: Dict the main data structure.
    """
    for key in article:
        if key in data:
            data[key].append(article[key])

    logger.info(f"Succesfuly scraped '{article["link"]}'\n")


def get_index(data, link):
    """
    Get the index of the article that matches the link.

    :param data: Dict the main data structure
    :param link: Article URL.
    :return: int, index of article in `data`
    """
    return data["link"].index(link)


def link_visited(data, link, category):
    """
    Checks if a link has been scraped or is known to be outdated.
    If already scraped; compares the current category to the category of the
    scraped article and adds the current category if they don't match.

    :param data: Dict main data structure.
    :param link: Article URL.
    :param category: Article category.
    :return: True if link is visited/outdated, False otherwise.
    """
    if link in data["link"]:
        index = get_index(data, link)
        cat = data["category"][index]
        if category not in cat:
            logger.warning(f"Existing: under {cat}, added {category} {link}\n")            
            data["category"][index] += f" {category}"
        logger.warning(f"Existing: under {cat} {link}\n")
        return True
    if link in data["outdated_links"]:
        logger.warning(f"OOD: from memory {link}\n")
        return True
    return False


def tolerance_limit_reached(data, link, links, index, tolerance):
    tolerance -= 1
    if tolerance == 0:
        data["outdated_links"] += links[index:]
        logging.warning(f"OOD: tolerance limit reached {link}\n")
        return True
    data["outdated_links"].append(link)
    logging.warning(f"OOD: {link}\n")
    return False

