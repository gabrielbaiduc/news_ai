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

# # Requests session and random user agents, used to avoid 403 when fetching html content
# user_agents = [
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
#     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
#     'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/86.0.4240.93 Mobile/15E148 Safari/604.1',
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
#     "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.57",
#     "Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36",
#     "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
#     "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
#     "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
#     "Mozilla/5.0 (X11; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36 OPR/49.0.2725.64"
# ]

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

# OpenAI API key and header 
api_key = "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"
openai_headers = {"Authorization": f"Bearer {api_key}"}
openai_endpoint = "https://api.openai.com/v1/chat/completions"
gpt_model = "gpt-3.5-turbo-0125"

