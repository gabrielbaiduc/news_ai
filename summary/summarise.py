from utils.web_operations import post
from utils.helpers import isinwindow, word_count
from data_manager.manager import *
from config.settings import *
import math

logger = logging.getLogger(__name__)

def calculatesummarylength(x):
	return round(40 + 65.24*math.log(0.01*x))

def compose_prompt(body, body_count):
	system_prompt = (
	    f"You will be given an article. Your task is to summarise it in "
	    f"'{calculatesummarylength(body_count)} words'."
	)

	data = {
	  "model": summary_model,
	  "messages": [{
	      "role": "system",
	      "content": system_prompt
	  }, {
	      "role": "user",
	      "content": body
	  }],
	  "temperature": 0.5,
	  "max_tokens": 1000,
	  "top_p": 1.0,
	  "frequency_penalty": 0.0,
	  "presence_penalty": 0.0
	}
	return data


def process_response(response, url, articles):
	response_dict = response.json()
	summary = response_dict["choices"][0]["message"]["content"]
	tokens_sent = response_dict["usage"]["prompt_tokens"]
	tokens_received = response_dict["usage"]["completion_tokens"]
	articles[url]["summary"] = summary
	articles[url]["tokens_sent"] = tokens_sent
	articles[url]["tokens_received"] = tokens_received
	articles[url]["summarised"] = True
	articles[url]["summary_count"] = word_count(summary)


def get_summary():
	articles = load_data()
	inwindow = isinwindow(articles)
	for url, article in inwindow.items():
		if not article["summarised"]:
			body = article["body"]
			count = article["body_count"]
			prompt = compose_prompt(body, count)
			response = post(prompt)
			if response is not None:
				logger.info(f"Response received, processing response for {url}")
				process_response(response, url, articles)
				logger.info(f"Summarised {url}")
	save_data(articles)

