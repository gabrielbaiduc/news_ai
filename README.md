# NewsAI

NewsAI is an end-to-end desktop application that seeks to streamline news consumption. It aggregates articles from NYTimes, APNews, and Al-Jazeera. These articles are then summarized using the OpenAI API, a premium service. The application groups articles by their similarities and merges the the grouped articles' summaries-using OpenAI API again-for a concise overview. Summaries are accessible via a straightforward desktop interface, where users can click on a summary to view the article's title, a link to the original piece, and its source. Articles are organized by region, facilitating a quick catch-up with global news. NewsAI allows users to browse through hundreds of articles in just 30 minutes, offering the option to delve deeper into intriguing topics by visiting the original articles. NewsAI runs locally, on your computer.

## First Launch

Upon the first launch, users are welcomed with a message and are prompted to input their OpenAI API key. Please have your key ready. The key is securely stored using your operating system's password manager. For adjustments, search for 'NewsAI' within your password manager. Initial setup, or re-initialization after a significant break, may take between 5-10 minutes as the application prepares the articles.
![Landing Screen](https://i.imgur.com/fs5onln.png)

## Notes

- **NYTimes Access:** The NYTimes website operates on a subscription model, offering a limited number of free articles. To access content beyond this quota via NewsAI, a subscription and login on your device are required.
  
- **OpenAI API Costs:** NewsAI utilizes the `gpt-3.5-turbo-0125` model from OpenAI, which is a paid service. For pricing details, please visit [OpenAI's pricing page](https://openai.com/pricing#language-models).

## Upcoming Features

### User Experience Enhancements

- **API Key Management:** Users will have the option to update their OpenAI API key.
- **Article Refresh:** A new button will refresh articles in the background, bringing new stories to the top and marking them for visibility.
- **Custom Summarization:** A toolkit for customizing how ChatGPT summarizes articles or selecting different model versions (default is gpt-3.5-turbo-0125).
- **Summary Grouping:** Implementation of an option to view individual summaries within merged article groups.
- **Analytics Dashboard:** Introduction of a window displaying various statistics about the articles for enhanced insight.

### Technical Improvements

- **Class Implementation:** Streamlining and enhancing class structures for better data management and operational efficiency.
- **Data Structure and Handling:** Refining the underlying data architecture for improved performance and reliability.
- **Documentation:** Enhanced docstrings and comments for better code clarity.
- **Content Filtering:** Improvements to the filtering process for links and article content.

## Future Directions

Given the challenges posed by copyright laws and the costs associated with OpenAI summarization, the development of these features remains uncertain. However, should there be significant interest from the open-source community and viable paths to address these challenges, I may pursue further development.

### Major Updates Considered

- **Expansion of Source Websites:** Potential inclusion of additional news outlets such as FT, WSJ, BBC, Politico, Economist, and others for broader coverage.
- **Topic Detection and Categorization:** Enhancing article grouping through advanced topic analysis, moving beyond predefined sections.
- **Advanced Scraping Framework:** Development of a machine learning-based framework for identifying and extracting article-like content from various web formats, inspired by the 'Newspapers' Python library.

## Installation

To use NewsAI, follow these steps:

### Step 1: Install Conda

If Conda is not already installed on your system, download it from either [miniconda](https://docs.anaconda.com/free/anaconda/install/index.html) or [miniforge](https://github.com/conda-forge/miniforge) and follow the instructions. Miniforge is recommended, but either will suffice. Alternatively, you can use Anaconda.

### Step 2: Create Your Virtual Environment

With Conda installed, open your command line interface and navigate to the NewsAI program folder. Create the environment with the following command:

```conda env create -f environment.yml```

### Step 3: Activate Your Virtual Environment
Activate the newly created environment:

```conda activate newsai```

To start NewsAI, ensure you are in the program folder and execute:

```python newsai.py```
