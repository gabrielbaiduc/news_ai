from config.settings import summary_model
from utils.web_operations import post


def compose_prompt(text, word_count):
	if word_count < 200:
		system_prompt = "appropriate system prompt"
	elif word_count < 500:
		system_prompt = "appropriate system prompt"
	else:
		system_prompt = "appropriate system prompt"
	max_tokens = 1.3*(word_count)*0.3

	data = {
	  "model": summary_model,
	  "messages": [{
	      "role": "system",
	      "content": system_prompt
	  }, {
	      "role": "user",
	      "content": text
	  }],
	  "temperature": 1,
	  "max_tokens": max_tokens,
	  "top_p": 1.0,
	  "frequency_penalty": 0.0,
	  "presence_penalty": 0.0
	}


def process_response(response, articles):
	response_dict = response.json()
	summary = response_dict["choices"][0]["message"]["content"]
	tokens_sent = response_dict["usage"]["prompt_tokens"]
	tokens_received = response_dict["usage"]["completion_tokens"]
	articles["summary"].append(summary)
	articles["tokens_sent"].append(tokens_sent)
	articles["tokens_received"].append(tokens_received)


def get_summary(articles):
	for text, word_count in zip(articles["text"], articles["word_count"]):
		prompt = compose_prompt(text, word_count)
		response = post(prompt)
		if response is not None:
			process_response(response, articles)

