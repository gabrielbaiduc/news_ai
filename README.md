# NewsAI
An application that scrapes articles from a few 'static' websites (NYTimes, APNews, and Al-Jazeera), summarizes them with the OpenAI API (a paid service), then groups each article based on similarity and merges the summaries of the grouped articles. Finally, the summaries are displayed via a simple desktop application. For each summary, you can access its title with a link back to the original article and the source of the article by clicking on the summary. The articles are categorized by region. Its purpose is to streamline and shorten the act of catching up with the news. It gives you the ability to scan through hundreds of articles in 30 minutes, with the option of diving deeper into topics of interest by reading the original article.

When launched for the first time, you'll be greeted with a welcome message and prompted to enter your OpenAI API key, so have it ready. Your key is saved using your operating system's password manager (change your key here if you want to, search for 'NewsAI'). On initial launch (or after longer breaks), the preparation of articles can take anywhere between 5-10 minutes.

# Notes:
The NYTimes is a subscription-based service with a quota of free articles. If you want to read beyond the free quota using NewsAI, you must subscribe and log in on your computer.

OpenAI's API is a paid service. The app uses the `gpt-3.5-turbo-0125` model. For more info on pricing, visit [OpenAI](https://openai.com/pricing#language-models).

Planned user experience updates:
- Ability to change the API key
- Add a refresh button that updates articles in the background and pushes them to the top (visually flagging new articles)
- Add a toolkit that allows users to customize how ChatGPT summarizes the articles or change model types (currently uses gpt-3.5)
- Implement a solution so that grouped articles with merged summaries have the option to show the individual summaries of all the components
- Add an Analytics window that shows various statistics about the articles
  
Planned technical updates:
- Improve class implementation them better (e.g., combined web operations, combined scraping and summary operations)
- Improve data structure and handling
- Cleaner docstrings and comments
- Improve filtering on link and content scraping

Below are a few major update ideas that I have. The chance that I'll develop them is small, for two reasons: copyright laws and the prohibitive cost of summarization via OpenAI. As it stands, this is an open-source portfolio project that I work on in my free time. If there is substantial interest in the app from the open-source community and there are ways to overcome the above concerns, I'll be more likely to invest more time in it.

A major planned update—if I get around to it—would be to introduce more static websites that can be scraped, like FT, WSJ, BBC, Politico, Economist, IndiaTimes, GlobalTimes, TheTimes, Guardian, BuzzFeed, Euronews, and more regional English language papers. Add these as options for users.

Another major update idea is the introduction of topic detection and categorization. This is an extension of the grouping concept, where articles are scraped without regard to what section they were scraped from. Instead, the categories are inferred from the text.

Lastly, I'd like to develop a separate framework to scrape articles. Inspired by the Python library 'Newspapers', it would utilize ML to recognize HTMLs that contain article-like content and scrape the contents regardless of the unique HTML structure of the website. 'Newspapers' implements a heuristic approach where the general rules were discovered 'manually' and implemented as rules. The ML method has the added benefit of being able to scrape not just news sites but think tanks, magazines, or even blogs.

# Installation
You'll need to download this repository to your computer, and you'll need Conda installed on your computer. Download the repo; if you already have Conda installed, skip to Step 2.
### Step 1: Install Conda
To install Conda, visit either [miniconda](https://docs.anaconda.com/free/anaconda/install/index.html) or [miniforge](https://github.com/conda-forge/miniforge) and follow the instructions. I recommend miniforge, but use whichever.

### Step 2: Create your virtual environment
Open your command line interface and navigate to the program folder, then type:

```conda env create -f environment.yml```

### Step 3: Activate your virtual environment
Once the dependencies are installed, type:

```conda activate newsai```

then (ensure you're in the program folder) type:

```python newsai.py```
