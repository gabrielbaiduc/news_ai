from scraping.scrapers import FetchHTML, ScrapeLinks, ScrapeContents
from data_manager.manager import DataManager
from config.settings import sections
import asyncio

# Initialise classes for scraping and managing the resulting data
manager = DataManager()
fetch = FetchHTML()
scrapelinks = ScrapeLinks()
scrapecontents = ScrapeContents()

# Fetch & parse section content
section_htmls = asyncio.run(fetch.fetch(sections))
parsed_section_htmls = fetch.parse(section_htmls)

# Scrape article links from sections
new_article_links = scrapelinks.scrape(parsed_section_htmls)

# Fetch & parse articles
article_htmls = asyncio.run(fetch.fetch(new_article_links))
parsed_article_htmls = fetch.parse(article_htmls)

# Scrape article contents
new_articles = scrapecontents.scrape(parsed_article_htmls)

# Save article contents by merging with existing contents
old_articles = manager.load()
merged_articles = manager.merge(old_articles, new_articles)
manager.save(merged_articles, "articles")
