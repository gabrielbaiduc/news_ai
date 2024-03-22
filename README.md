# NewsAI
An application that scrapes articles from a few 'static' websites (NYTimes, APNews and Al-Jazeera), summarises them with the OpenAI API (paid service), then groups each article based on how similar they are and merges the summaries of the grouped articles. Finally, the summaries are displayed via a simple desktop application. For each summary; you can access it's title with a link back to the original article and the source of the article by clicking on the summary. The articles are categorised by region. It's purpose is to streamline and shorten the act of cathcing up with the news. Gives you the ability to scan through hunderds of articles in 30 minutes with the option of diving deeper in topics of interests by reading the original article.

# Notes:
The NYTimes is subscription based service with a quota of free articles. If you want to read it, you must register, subscribe and log-in on your computer.

There are plans for numerous smaller improvements.
User-experience:
- ability to change API key
- in-app refresh that updates articles in the backgorund and pushes them to the top (visually flagging new articles)
- add add a toolkit that'd allow users to customize how ChatGPT summarizes the articles or change model types (uses gpt3.5 currently)
- implement a solution so that grouped articles with merged summaries have the option to show the individual summaries of all the components
- 
Technical:
- combine classes and implement them better (eg.: more efficient data management, combined web-operations, combined scraping and summary operations)
- cleaner docstrings and comments
- fucking fix the datastructure of articles
- improve filtering on link and content scraping

A major planned update - if I get around it - would be to introduce more static websites that can be scraped like BuzzFeed, euronews, FT, WSJ, BBC, Politico, Economist, IndiaTimes, GlobalTimes, TheTimes, Guardian, and more regional english language papers. Add these as option for users. This would include extendending the concurrecy of the code, potentially introducing threading so that articles can be scraped and summarised concurrently because if all sources are selected, we're talking about 1000s of articles every day. Not to mention that the cost of summaries would be more than the subscription fees. But, prices may go down in the future. 

Another major update idea is the introduction of topic detection and categorisation. This is an extension of the grouping concept, where articles are scraped without regards to what section they were scraped from. Insead, the text is analysed and categories are inferred. This could introduce options for custom category creation where you enter "elections 2024" and hundreds of relevant articles from two-dozen different news-sites are summarised. This would likely require a team, but let's see.

Last major update, that probably will never come, is the introduction of ML models (likely transformers) that scrape article links and contents from HTMLs. This would require a huge effort, but the results could be fantastic; a well trained model could scrape any article-like content not just from news-sites but think-tanks, open-source publishing sites, magazines, blogs and others. I say that it'll never come because something like this requires consisents team effort for as long as it's operational due to the nature of unstructured internet-data. Once developed, no-one would publish it freely given the value of such data. Never-the-less, the day might come, so I'll leave it here as a reminder.

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

