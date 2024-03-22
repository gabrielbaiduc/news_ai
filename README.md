# NewsAI
An end-to-end project that I created for fun. The program scrapes articles from a few static websites (NYTimes, APNews and Al-Jazeera), summarises them with the OpenAI API (paid service), then groups each article based on how similar they are and merges the summaries of the grouped articles. Finally, the summaries are displayed via a simple desktop application. For each summary; you can access it's title with a link back to the original article and the source of the article by clicking on the summary. 

I've had my mind to built something comprehensive related to analysing news. I've also been hearing a lot of good things about ChatGPT so I came up with this idea to work on that combines both aspects.

## Notes:
This is by no means a complete, user-ready program. There are countless opportunities for improvement, I recognise that. My goal was never to build a perfect app but to build something that works. I also wanted to make something slick and easily accessible.

The major lesson I walk away with is that data is everything. I've spent 90% of my development time working with data. It's the part of the program that was the hardest to get right - or even just to get it working. I've had numerous ideas on how to implement certain things better while coding. Initially, I followed them up, but as I progressed, I just ended up jotting them down somewhere and moving on. Each new idea would've pushed my deployment up by weeks or months. Data mining, engineering, wrangling, massaging or whatever else you call it, is the essence of ML. I feel good about having had this realisation. It seems to be a recurring theme so I'm looking forward for my next project that is likely to be focused solely on data.

# Installation
You'll need 'conda' installed on your computer to run this program. If you already have 'conda' skip to step 2.
### Step 1
Install conda via the <a>'miniconda'</a> or 'miniforge' distributions. I recommend the 'miniforge'.
