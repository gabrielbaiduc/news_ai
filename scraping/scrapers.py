import logging
import random
import aiohttp
# from aiohttp import TCPConnector
import asyncio
from collections import defaultdict
from urllib.parse import urljoin
import json
from dateutil import parser
from dateutil import tz
from collections import Counter

from bs4 import BeautifulSoup

from config.settings import selectors
from config.settings import user_agents
from utils.helpers import isoutdated
from data_manager.manager import DataManager


logger = logging.getLogger(__name__)



class FetchHTML:
    def __init__(self, rate_limit=50):
        self.rate_limit = rate_limit
        self.user_agents = user_agents
        self.exceptions = []

    async def fetch(self, urls):
        connector = aiohttp.TCPConnector(limit=self.rate_limit)
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = [self._process_url(url, src, cat, session) 
                     for url, src, cat in urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            results = self._sort_results(results)
            logger.info(f"Fetched HTML of {len(results)} URLs from "
                f"{len(tasks)} concurrent tasks with "
                f"{len(self.exceptions)} exceptions"
                )
            return results

    def parse(self, results):
        parsed = []
        for url, src, cat, html in results:
            soup = BeautifulSoup(html, "html.parser")
            parsed.append((url, src, cat, soup))
            logger.debug(f"Parsed HTML of {url}")
        logger.info(f"Parsed HTML of {len(parsed)} URLs.")
        return parsed

    def _sort_results(self, results):
        success = []
        for result in results:
            if isinstance(result, Exception):
                self.exceptions.append(result)
            else:
                success.append(result)
        return success

    async def _process_url(self, url, src, cat, session):
        html = await self._fetcher(url, session)
        return (url, src, cat, html)

    async def _fetcher(self, url, session):
        headers = {'User-Agent': self.get_random_user_agent()}
        try:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                logger.debug(f"Fetched HTML of {url}.")
                return await response.text()
        except aiohttp.ClientResponseError as error:
            logger.error(f"{error.status} {error.message} {url}")
            raise

    def get_random_user_agent(self):
        """
        Selects a random user agent from the list.
        Returns:
            str: A random user agent string.
        """
        return random.choice(self.user_agents)

    

class ScrapeLinks:
    def __init__(self):
        self.manager = DataManager()
        self.articles = self.manager.load()
        self.discarded = self.manager.load("discarded")
        self.link_selector = selectors["link_selector"]
        self.link_prefix = selectors["link_prefix"]
        self.links_count = defaultdict(int)

    def scrape(self, parsed):
        new_links = []
        logger.debug(f"Scraping {len(parsed)} URLs")
        for url, src, cat, soup in parsed:
            elements = self._getelements(soup, src, url)
            if not elements:
                continue
            hrefs = self._gethrefs(elements, src)
            links = self._construct_links(hrefs, src)
            links = self._check_processed(links)
            if not links:
                logger.debug(f"No new links from {url} check ScrapeLinks")
                continue
            links = [(link, src, cat) for link in links]
            self.links_count[src] += len(links)
            new_links.extend(links)
            logger.debug(f"Scraped {len(links)} new links from {url}")
        checked_links = self._check_category(new_links)
        return checked_links

    def _check_category(self, links):
        temp = {}
        for link, src, cat in links:
            if link in temp and cat not in temp[link]["cats"]:
                temp[link]["cats"].append(cat)
                logger.debug(f"Added category {link}")
            elif link in temp and cat in temp[link]["cats"]:
                logger.debug(f"Duplicate {link}")
                continue
            elif link not in temp:
                temp[link] = {"src": src, "cats": [cat]}
        return [
        (link, info['src'], info['cats']) for link, info in temp.items()
        ]

    def _getelements(self, soup, src, url):
        selector = self.link_selector[src]
        elements = soup.select(selector)
        if elements:
            return elements
        logger.error(f"Link Selector is broken {src} {selector} {url}")

    def _gethrefs(self, elements, src):
        hrefs = [
            element["href"] for element in elements if element.get("href")
        ]
        if src == "NYTimes":
            hrefs = self._check_nyt_notarticle(hrefs)
        return hrefs

    def _construct_links(self, hrefs, src):
        prefix = self.link_prefix[src]
        return [urljoin(prefix, href) for href in hrefs]

    def _check_nyt_notarticle(self, hrefs):

        return [
            href for href in hrefs
            if not href.startswith("/interactive")
            and not href.startswith("/video")
        ]

    def _check_processed(self, links):
        if self.articles:
            processed = [article["url"] for article in self.articles]
            filtered = [link for link in links if 
            link not in processed and link not in self.discarded
            ]
            logger.debug(f"Filtered {len(links)-len(filtered)} links from "
                f"{len(links)}."
            )
            return filtered
        else:
            return links

    def getfeature(feature):
        return [a[faeture] for a in data]
    
        return flist

    def _count_newlinks(self, new_links):
        counter = Counter([a[1] for a in new_links])
        logger.info(f"New links:")
        [logger.info(f"{v, c}") for v, c in counter.items()]


class ScrapeContents:
    def __init__(self):
        self.manager = DataManager()
        self.discarded = self.manager.load("discarded")
        self.header_selector = selectors["header_selector"]
        self.text_selector = selectors["text_selector"]

    def scrape(self, parsed):
        logger.debug(f"Scraping {len(parsed)} URLs")
        articles = []
        for url, src, cat, soup in parsed:
            header = self._getheader(soup, src, url)
            if not header or self._check_notarticle(header, url):
                self._discard(url)
                continue
            header_contents = self._getheader_contents(header, url)
            if not header_contents:
                self._discard(url)
                continue
            pub, mod, hline, desc = header_contents
            if isoutdated(pub):
                self._discard(url)
                logger.debug(f"Outdated {url}")
                continue
            body = self._getbody(soup, src, url)
            if not body:
                self._discard(url)
                continue
            article = self._buildarticle(
                url, src, cat, pub, mod, hline, desc, body
                )
            articles.append(article)
            logger.info(f"Scraped article from {url}")
        self.manager.save(self.discarded, "discarded")
        logger.info(f"Scraped {len(articles)} new articles from {len(parsed)} "
            f"links")
        return articles
    
    def _getheader(self, soup, src, url):
        selector = self.header_selector[src]
        element = soup.select_one(selector)
        if not element:
            logger.error(f"Header selector is broken: {src} {selector} {url}")    
            return None
        string = element.get_text()
        try:
            header = json.loads(string)
        except JSONDecodeError as error:
            logger.error(f"Header is not in JSON format: {error}")
            return None
        if isinstance(header, list):
            header = header[0]
        logger.debug(f"Scraped header of {url}")
        return header

    def _getheader_contents(self, header, url):
        try:
            pub = self._parse_datetime(header["datePublished"])
            mod = self._parse_datetime(header["dateModified"])
            hline = header["headline"]
            desc = header["description"]
            logger.debug(f"Scraped header contents of {url}")
            return pub, mod, hline, desc
        except KeyError as error:
            logger.error(
                f"Header key {error} is broken or not an article: {url}"
                )
            return None
    
    def _getbody(self, soup, src, url):
        selector = self.text_selector[src]
        elements = soup.select(selector)
        if not elements:
            logger.error(f"Text selector is broken: {url} {selector}")
            return None
        paragraphs = [element.text.strip() for element in elements]
        logger.debug(f"Scraped {len(paragraphs)} paragraphs ... ")
        paragraphs = [p for p in paragraphs if len(p.split()) > 0]
        logger.debug(f"... of which {len(paragraphs)} is non-empty.")
        body = " ".join(paragraphs)
        if len(body.split()) < 100:
            logger.warning(f"Body too short or not an article: {url}")
            return None
        logger.debug(f"Scraped body of {url}.")
        return body
        
    def _parse_datetime(self, string):
        """
        Parses and standardizes the article's publication and modification
        datetime strings to UTC.
        """
        parsed_datetime = parser.isoparse(string)
        standardised_datetime = parsed_datetime.astimezone(tz.tzutc())
        return standardised_datetime

    def _check_notarticle(self, header, url):
        """
        Checks if the article header indicates that the content is not a
        standard article, such as a video.
        """
        if header.get("@type") == "VideoObject":
            logger.warning(f"Not an article {url}")
            return True
        return False

    def _buildarticle(self, url, src, cat, pub, mod, hline, desc, body):
        """
        Constructs a dictionary representing the article with all relevant
        details.
        """
        return {
            "bodycount": len(body.split()),
            "source": src,
            "category": cat,
            "headline": hline,
            "published": pub,
            "modified": mod,
            "url": url,
            "description": desc,
            "body": body,
        }

    def _discard(self, url):
        self.discarded.append(url)
        logger.info(f"Discarded {url}")