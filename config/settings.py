from datetime import datetime


# Initialise global variables
today = str(datetime.now().date())
ood_tolerance = 5

# Keys for main data structure
data_keys = [
        "title",
        "text",
        "date",
        "link",
        "source",
        "category",
        "word_count",
        "outdated_links"
]

# Requests session and random user agents, used to avoid 403 when fetching html content
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/86.0.4240.93 Mobile/15E148 Safari/604.1',
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.57",
    "Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (X11; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36 OPR/49.0.2725.64"
]

# Section URLs and the categories they belong to
section_configs = {
    "bbc": [
        ("https://www.bbc.com/news/world/africa", "africa"),
        ("https://www.bbc.com/news/world/asia", "asia"),
        ("https://www.bbc.com/news/world/australia", "asia"),
        ("https://www.bbc.com/news/world/europe", "europe"),
        ("https://www.bbc.com/news/world/latin_america", "americas"),
        ("https://www.bbc.com/news/world/middle_east", "middle_east"),
        ("https://www.bbc.com/news/world/us_and_canada", "north_america"),
        ("https://www.bbc.com/news/uk", "europe")
    ],
    "nyt": [
        ("https://www.nytimes.com/section/world/africa", "africa"),
        ("https://www.nytimes.com/section/world/australia", "asia"),
        ("https://www.nytimes.com/section/world/americas", "americas"),
        ("https://www.nytimes.com/section/world/asia", "asia"),
        ("https://www.nytimes.com/section/world/canada", "north_america"),
        ("https://www.nytimes.com/section/world/europe", "europe"),
        ("https://www.nytimes.com/section/world/middleeast", "middle_east"),
        ("https://www.nytimes.com/section/us", "north_america")
    ],
    "aj": [
        ("https://www.aljazeera.com/africa", "africa"),
        ("https://www.aljazeera.com/asia-pacific", "asia"),
        ("https://www.aljazeera.com/asia", "asia"), 
        ("https://www.aljazeera.com/europe", "europe"),
        ("https://www.aljazeera.com/latin-america", "americas"),
        ("https://www.aljazeera.com/middle-east", "middle_east"),
        ("https://www.aljazeera.com/us-canada", "north_america")
    ]
}

# CSS selectors grouped by source
selector_configs = {
    "bbc": {
        "link_selector": "ol.e1y4nx260 div[type='article'] a.ej9ium92",
        "link_prefix": "https://www.bbc.com",
        "title_selector": "article h1",
        "text_selector": "article div[data-component='text-block']",
        "date_selector": "article time"
    },
    "nyt": {
        "link_selector": "article a.css-1u3p7j1, article a.css-8hzhxf",
        "link_prefix": "https://www.nytimes.com",
        "title_selector": "article[id='story'] h1",
        "text_selector": "article[id='story'] section[name='articleBody'] p.css-at9mc1",
        "date_selector": "article[id='story'] time"
    },
    "aj": {
        "link_selector": "div.container__inner article.gc--type-post h3 a",
        "link_prefix": "https://www.aljazeera.com",
        "title_selector": "main header h1",
        "text_selector": "main div.wysiwyg p",
        "date_selector": "main div.article-info-block span[aria-hidden=\"true\"]"
    }
}

# Selector error messages
selector_error_messages = ["date selector error", "title selector error", "text selector error"]



