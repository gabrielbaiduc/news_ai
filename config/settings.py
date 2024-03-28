# Configuration data for operations across the program. 
# The 'sections' and 'selectors' are used in scraping and define the logic of 
# the program. The sections list contain urls of sections within news-sites.
# Each section url is grouped by source and category, where the category is a 
# somewhat arbitrary choice that I made. Eg.: I choose to put
# Australia section to Asia which is arbitrary. Also, using CSS 
# selectors to scrape article links and contents is not the best. 
# I recognise that this is a very static, stiff and fragile solution to 
# scraping articles. 

# I decided to include the category and source information of each section 
# because it made scrapin easier. The categories are used to group the articles
# when displayed. The sources are used to navigate the custom selectors. Again,
# this is a clunky solution that introduces a bunch of loops and tuple unpacking
# but it made the implementation simpler. In an ideal world I have a set of 
# heuristcs applicable for most news-sites where source doesn't have to be 
# tracked. I'd also have a topic modelling algorithm with keyword extraction 
# that automatically categorises the articles in a more organic way. 

# NOTE: the best and most elegant solution would be to train one or two 
# transformers that can extract article links and contents from parsed
# (or unparsed) HTML data. Then, implement a crawler that crawls the front-page
# and sections of news-sites and creates a data-loop with the model(s). The 
# crawler fetches HTMLs for the models. The models either extract links that are 
# passed to the crawler or contents which are stored. Upload the program to a 
# server, implement careful rate-limiting and depth-limiting for the crawler and
# you have a system that can scrape a huge number of news-sites 24/7, keeping
# a comprehensive stockpile of the freshest articles that can be used for 
# analytics and display.

# ToDo:
# 1) Add more sources

# List of urls grouped by source and custom category. 
sections =[
        # ("https://www.bbc.com/news/world/africa", "BBCNews","Africa"),
        # ("https://www.bbc.com/news/world/asia", "BBCNews", "Asia"),
        # ("https://www.bbc.com/news/world/australia", "BBCNews", "Asia"),
        # ("https://www.bbc.com/news/world/europe", "BBCNews", "Europe"),
        # ("https://www.bbc.com/news/world/latin_america", "BBCNews", "Americas"),
        # ("https://www.bbc.com/news/world/middle_east", "BBCNews", "Middle-East"),
        # ("https://www.bbc.com/news/world/us_and_canada", "BBCNews", "North-America"),
        # ("https://www.bbc.com/news/uk", "BBCNews", "Europe"),
        ("https://www.nytimes.com/section/world/africa?page=2", "NYTimes", 
            "Africa"),
        ("https://www.nytimes.com/section/world/australia?page=2", "NYTimes", 
            "Asia"),
        ("https://www.nytimes.com/section/world/americas?page=2", "NYTimes", 
            "Americas"),
        ("https://www.nytimes.com/section/world/asia?page=2", "NYTimes", 
            "Asia"),
        ("https://www.nytimes.com/section/world/canada?page=2", "NYTimes", 
            "North-America"),
        ("https://www.nytimes.com/section/world/europe?page=2", "NYTimes", 
            "Europe"),
        ("https://www.nytimes.com/section/world/middleeast?page=2", "NYTimes",
         "Middle-East"),
        ("https://www.nytimes.com/section/us?page=5", "NYTimes", 
            "North-America"),
        ("https://www.aljazeera.com/africa", "AlJazeera", "Africa"),
        ("https://www.aljazeera.com/asia-pacific", "AlJazeera", "Asia"),
        ("https://www.aljazeera.com/asia", "AlJazeera", "Asia"), 
        ("https://www.aljazeera.com/europe", "AlJazeera", "Europe"),
        ("https://www.aljazeera.com/latin-america", "AlJazeera", "Americas"),
        ("https://www.aljazeera.com/middle-east", "AlJazeera", "Middle-East"),
        ("https://www.aljazeera.com/us-canada", "AlJazeera", "North-America"),
        ("https://apnews.com/politics", "APNews", "North-America"),
        ("https://apnews.com/hub/asia-pacific", "APNews", "Asia"),
        ("https://apnews.com/hub/latin-america", "APNews", "Americas"),
        ("https://apnews.com/hub/europe", "APNews", "Europe"),
        ("https://apnews.com/hub/africa", "APNews", "Africa"),
        ("https://apnews.com/hub/middle-east", "APNews", "Middle-East"),
        ("https://apnews.com/hub/china", "APNews", "Asia"),
        ("https://apnews.com/hub/australia", "APNews", "Asia")
]

# Selectors for links, link prefixes, article text and header element
selectors = {
    "link_selector": {
        "BBCNews": "div[data-testid='alaska-section'] a",
        "NYTimes": "section#stream-panel li article a.css-8hzhxf",
        "AlJazeera": "div.container__inner article.gc--type-post h3 a",
        "APNews": "div.Page-content div.PageList-items-item h3 a"
    },
    "link_prefix": {
        "BBCNews": "https://www.bbc.com",
        "NYTimes": "https://www.nytimes.com",
        "AlJazeera": "https://www.aljazeera.com",
        "APNews": "",
    },
    "text_selector": {
        "BBCNews": "section[data-component='text-block']",
        "NYTimes": "article[id='story'] section[name='articleBody'] p.css-at9mc1",
        "AlJazeera": "main#main-content-area div.wysiwyg p",
        "APNews": "main div.RichTextBody p"
    },
    "header_selector": {
        "BBCNews": "script[type='application/ld+json']",
        "NYTimes": "script[type='application/ld+json']",
        "AlJazeera": "script[type='application/ld+json']",
        "APNews": "script[type='application/ld+json']"
    }
}

# List of user agents used for rotating user agents when fetching HTML of 
# news sites
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
    "like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/14.0 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1"
    ".15 (KHTML, like Gecko) CriOS/86.0.4240.93 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
    "like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 "
    "Firefox/86.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.57",
    "Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, "
    "like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1"
    ".15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (X11; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
    "like Gecko) Chrome/62.0.3202.94 Safari/537.36 OPR/49.0.2725.64"
]

# Keyring constats for storing and retrieving the OpenAI API key
kr_system = "NewsAI"
kr_username = "openai_api_key"

# Parameter grid for the custom parameter search in 'grouping/group.py'
parameter_grid = {
    'eps': [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    "n_components": [70, 90, 110, 130, 150]
}

# System prompt for merging.