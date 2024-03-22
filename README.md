# NewsAI
An end-to-end project that I created for fun. The program scrapes articles from a few static websites (NYTimes, APNews and Al-Jazeera), summarises them with the OpenAI API (paid service), then groups each article based on how similar they are and merges the summaries of the grouped articles. Finally, the summaries are displayed via a simple desktop application. For each summary; you can access it's title with a link back to the original article and the source of the article by clicking on the summary. 

I've had my mind to built something comprehensive related to analysing news. I've also been hearing a lot of good things about ChatGPT so I came up with this idea to work on that combines both aspects.

## Notes:
This is by no means a complete, user-ready program. There are countless opportunities for improvement, I recognise that. My goal was never to build a perfect app but to build something that works. I also wanted to make something slick and easily accessible.

A notable lesson I walk away with is recognition of the importance of data in this field. I've spent 90% of my development-time working with data. Every part of the program that was the hardest to get right - or even just to get to work - are related to data.

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

