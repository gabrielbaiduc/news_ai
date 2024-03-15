

# Section URLs and the categories they belong to
section_configs = {
    "bbc": [
        ("https://www.bbc.com/news/world/africa", "Africa"),
        ("https://www.bbc.com/news/world/asia", "Asia"),
        ("https://www.bbc.com/news/world/australia", "Asia"),
        ("https://www.bbc.com/news/world/europe", "Europe"),
        ("https://www.bbc.com/news/world/latin_america", "Americas"),
        ("https://www.bbc.com/news/world/middle_east", "Middle-East"),
        ("https://www.bbc.com/news/world/us_and_canada", "North-America"),
        ("https://www.bbc.com/news/politics", "Europe")
    ],
    "nyt": [
        ("https://www.nytimes.com/section/world/africa?page=2", "Africa"),
        ("https://www.nytimes.com/section/world/australia?page=2", "Asia"),
        ("https://www.nytimes.com/section/world/americas?page=2", "Americas"),
        ("https://www.nytimes.com/section/world/asia?page=2", "Asia"),
        ("https://www.nytimes.com/section/world/canada?page=2", "North-America"),
        ("https://www.nytimes.com/section/world/europe?page=2", "Europe"),
        ("https://www.nytimes.com/section/world/middleeast?page=2", "Middle-East"),
        ("https://www.nytimes.com/section/us?page=5", "North-America")
    ],
    "aj": [
        ("https://www.aljazeera.com/africa", "Africa"),
        ("https://www.aljazeera.com/asia-pacific", "Asia"),
        ("https://www.aljazeera.com/asia", "Asia"), 
        ("https://www.aljazeera.com/europe", "Europe"),
        ("https://www.aljazeera.com/latin-america", "Americas"),
        ("https://www.aljazeera.com/middle-east", "Middle-East"),
        ("https://www.aljazeera.com/us-canada", "North-America")
    ],
    "ap": [
        ("https://apnews.com/politics", "North-America"),
        ("https://apnews.com/hub/asia-pacific", "Asia"),
        ("https://apnews.com/hub/latin-america", "Americas"),
        ("https://apnews.com/hub/europe", "Europe"),
        ("https://apnews.com/hub/africa", "Africa"),
        ("https://apnews.com/hub/middle-east", "Middle-East"),
        ("https://apnews.com/hub/china", "Asia"),
        ("https://apnews.com/hub/australia", "Asia")
    ]
}

# CSS selectors grouped by source
selector_configs = {
    "ld_json": "script[type='application/ld+json']",
    "bbc": {
        "link_selector": "div[data-testid='alaska-section'] a",
        "link_prefix": "https://www.bbc.com",
        # "title_selector": "article h1",
        "text_selector": "section[data-component='text-block'] p",
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
api_key = "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"

short_prompt = "You will be given an article. Your task is to summarise it in '1 sentence.'"
medium_prompt = "You will be given an article. Your task is to summarise it in '2 sentences."
long_prompt = "You will be given an article. Your task is to summarise it in '1 paragraph'."

# OpenAI model
summary_model = "gpt-3.5-turbo-0125"

