

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
        ("https://www.bbc.com/news/politics", "europe")
    ],
    "nyt": [
        ("https://www.nytimes.com/section/world/africa?page=2", "africa"),
        ("https://www.nytimes.com/section/world/australia?page=2", "asia"),
        ("https://www.nytimes.com/section/world/americas?page=2", "americas"),
        ("https://www.nytimes.com/section/world/asia?page=2", "asia"),
        ("https://www.nytimes.com/section/world/canada?page=2", "north_america"),
        ("https://www.nytimes.com/section/world/europe?page=2", "europe"),
        ("https://www.nytimes.com/section/world/middleeast?page=2", "middle_east"),
        ("https://www.nytimes.com/section/us?page=5", "north_america")
    ],
    "aj": [
        ("https://www.aljazeera.com/africa", "africa"),
        ("https://www.aljazeera.com/asia-pacific", "asia"),
        ("https://www.aljazeera.com/asia", "asia"), 
        ("https://www.aljazeera.com/europe", "europe"),
        ("https://www.aljazeera.com/latin-america", "americas"),
        ("https://www.aljazeera.com/middle-east", "middle_east"),
        ("https://www.aljazeera.com/us-canada", "north_america")
    ],
    "ap": [
        ("https://apnews.com/politics", "north_america"),
        ("https://apnews.com/hub/asia-pacific", "asia"),
        ("https://apnews.com/hub/latin-america", "americas"),
        ("https://apnews.com/hub/europe", "europe"),
        ("https://apnews.com/hub/africa", "africa"),
        ("https://apnews.com/hub/middle-east", "middle_east"),
        ("https://apnews.com/hub/china", "asia"),
        ("https://apnews.com/hub/australia", "asia")
    ]
}

# CSS selectors grouped by source
selector_configs = {
    "ld_json": "script[type='application/ld+json']",
    "bbc": {
        "link_selector": "ol.e1y4nx260 div[type='article'] a.ej9ium92",
        "link_prefix": "https://www.bbc.com",
        # "title_selector": "article h1",
        "text_selector": "article div[data-component='text-block']",
        # "date_selector": "article time"
    },
    "nyt": {
        "link_selector": "section#stream-panel li article a.css-8hzhxf",
        "link_prefix": "https://www.nytimes.com",
        # "title_selector": "article[id='story'] h1",
        "text_selector": "article[id='story'] section[name='articleBody'] p.css-at9mc1",
        # "date_selector": "article[id='story'] time"
    },
    "aj": {
        "link_selector": "div.container__inner article.gc--type-post h3 a",
        "link_prefix": "https://www.aljazeera.com",
        # "title_selector": "main header h1",
        "text_selector": "main#main-content-area div.wysiwyg p",
        # "date_selector": "main div.article-info-block span[aria-hidden=\"true\"]"
    },
    "ap": {
        "link_selector": "div.Page-content div.PageList-items-item h3 a",
        "link_prefix": "",
        "text_selector": "main div.RichTextBody p"
    }
}

# Selector error messages
selector_error_messages = ["date selector error", "title selector error", "text selector error"]

# OpenAI API key and header 
api_key = "my api key"

# OpenAI model
summary_model = "gpt-3.5-turbo-0125"

