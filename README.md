# NewsAI
An application that scrapes articles from a few 'static' websites (NYTimes, APNews and Al-Jazeera), summarises them with the OpenAI API (paid service), then groups each article based on how similar they are and merges the summaries of the grouped articles. Finally, the summaries are displayed via a simple desktop application. For each summary; you can access it's title with a link back to the original article and the source of the article by clicking on the summary. The articles are categorised by region. It's purpose is to streamline and shorten the act of cathcing up with the news. Gives you the ability to scan through hunderds of articles in 30 minutes with the option of diving deeper in topics of interests by reading the original article.

When launched for the first time you'll be greeted with a welcome message and prompted to enter you OpenAI API key so have it ready. Once you've enterd a valid API key it is saved to your OS-specific password manager (change your key here if you want to, search for 'NewsAI') and the program starts preparing you the articles. On initial launch (or after longer breaks) this can take anywhere between 5-10 minutes. 

# Notes:
The NYTimes is subscription based service with a quota of free articles. If you want to read beyont the free-quota using NewsAI, you must subscribe and log-in on your computer.

OpenAI's API is a paid service. The app uses the `gpt-3.5-turbo-0125` model. For more info on pricing visit <a href="https://openai.com/pricing#language-models">OpenAI</a>.

There are plans for numerous smaller improvements.
User-experience:
- ability to change API key
- add a refresh button that updates articles in the backgorund and pushes them to the top (visually flagging new articles)
- add a toolkit that'd allow users to customize how ChatGPT summarizes the articles or change model types (uses gpt3.5 currently)
- implement a solution so that grouped articles with merged summaries have the option to show the individual summaries of all the components
- add a Analytics window that shows various statistics about the articles
  
Technical:
- combine classes and implement them better (eg.: more efficient data management, combined web-operations, combined scraping and summary operations)
- cleaner docstrings and comments
- fucking fix the datastructure of articles
- improve filtering on link and content scraping

Bellow are a few major update ideas that I have. The chance that I'll develop them is small, for two reasons; copyright laws and the prohibitive cost of summarisation via OpenAI. As it stands, this is an open-source portfolio project that I work on in my free time. If there is substantial interest in the app from the open-source community and there are ways to overcome the above concerns, I'll be more likely to invest more time in it.

A major planned update - if I get around to it - would be to introduce more static websites that can be scraped like FT, WSJ, BBC, Politico, Economist, IndiaTimes, GlobalTimes, TheTimes, Guardian, BuzzFeed, euronews, and more regional english language papers. Add these as option for users.

Another major update idea is the introduction of topic detection and categorisation. This is an extension of the grouping concept, where articles are scraped without regards to what section they were scraped from. Instead, the categories are inferred from the text.

Lastly, I'd like to develop a separate framework to scrape articles. Inspired by the Python libary 'Newspapers', it would utilise ML to recognise HTMLs that contain article-like content and scrape the contents regardless of the unique HTML structure of the website. 'Newspapers' implements a heuristic approach where the general rules were discovered 'manually' and implemented as rules. The ML method has the added benefit of being able to scrape not just news-sites but think-tanks, magazines or even blogs.

# Installation
You'll need to download this repository to your computer and you'll need conda installed on your computer. Download the repo, if you already have conda installed, skip to Step 2.
### Step 1 Install Conda
To install conda visit either <a href="https://docs.anaconda.com/free/anaconda/install/index.html">miniconda</a> or <a href="https://github.com/conda-forge/miniforge">miniforge</a> and follow the instructions. I recommend mini-forge but use whichever.

### Step 2 Create your virtual environment
Open your command line interface and navigate to the program folder then type 

```conda env create -f environment.yml```

### Step 3 Activate your virtual envirnomen
Once the dependencies are installed, type:

```conda activate newsai```

then (ensure you're in the program folder) type:

```python newsai.py```

Give it a few minutes to do it's work. It takes longer on the first run as there are hundreds of articles to work through.

