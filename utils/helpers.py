import logging

logger = logging.getLogger(__name__)



def add_article(article, data):
    """
    Appends article information to the corresponding keys in the data dict.

    Parameters:
        article (dict): The article contents, keys correspond with 
        main data structure
        data (dict): The main data structure
    """
    for key in article:
        if key in data:
            data[key].append(article[key])

    logger.info(f"Succesfuly scraped '{article["link"]}'\n")


def get_index(data, link):
    """
    Get the index of the article in data that matches the link.

    Parameters:
        data (dict): The main data structure
        link (str): The article's URL.
    Return:
        (int): the index 
    """
    return data["link"].index(link)


def link_visited(data, link, category):
    """
    Checks if a link has been scraped or is known to be outdated.
    If already scraped; compares the current category to the category of the
    scraped article and adds the current category if they don't match.

    Parameters:
        data (dict): The main data structure.
        link (str): The articles URL.
        category (str): The category the article belongs to.
    Returns:
        (bool) True if link is visited/outdated, False otherwise.
    """
    if link in data["link"]:
        index = get_index(data, link)
        cat = data["category"][index]
        if category not in cat:
            logger.debug(f"Existing: under {cat}, added {category} {link}\n")            
            data["category"][index] += f" {category}"
        logger.debug(f"Existing: under {cat} {link}\n")
        return True
    if link in data["outdated_links"]:
        logger.debug(f"OOD: from memory {link}\n")
        return True
    return False


def tolerance_limit_reached(data, link, links, index, tolerance):
    """
    Checks if the tolearnce-limit on out-dated-articles in a list of links from
    a section is reached.

    Parameters:
        data (dict): The main data structure
        link (str): The URL of the article currently scraped
        links (list): The list of articles scraped from the current section
        index (int): The index of `link` in `links`
        tolerance (int): The number of consecutive out-of-date articles allowed
    """
    if tolerance == 0:
        data["outdated_links"] += links[index:]
        logging.warning(f"OOD: tolerance limit reached {link}\n")
        return True
    data["outdated_links"].append(link)
    logging.warning(f"OOD: {tolerance} after {link}\n")
    return False

