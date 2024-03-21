import re
from pathlib import Path

import nltk
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


class Preprocess:
	"""
	Class responsible for preprocessing article texts.
	It gathers all text data from an articles. The text is cleaned, 
	non-letter characters removed, single letters removed. The cleaned text is
	tokenized and lemmatized. Stop words are filtered out. 
	For lemmatization we assign treebank tags then convert them to wordnet tags.
	"""
	def __init__(self):
		self.base_dir = Path(__file__).resolve().parent.parent
		self.nltk_data_path = self.base_dir / "data" / "nltk_data"
		self._configure_nltk_data_path()
		self.stopwords = set(stopwords.words('english'))


	def process(self, articles):
		"""
			Main method that iterates over list of articles, extracts text and
			processes text. Lastly, it adds the processed text to the article
			dictionary.

			Params:
				articles (list): list of article dicts
		"""
		for article in articles:
			text = self.get_text(article)
			cleaned = self.clean(text)
			token_list = word_tokenize(cleaned)
			lemma_list = self.lemmatize(token_list)
			merged = " ".join(lemma_list)
			article["processed_text"] = merged


	def get_text(self, article):
		"""
		Takes an article dictionary as argument, returns the 'headline', 'body'
		and 'description' and 'summary' combined.
		"""
		text = " ".join((
			article["headline"],
			article["description"],
			article["body"],
			article["summary"]
			))
		return text

	def get_wordnet_pos(self, treebank_tag):
	    """
	    	Takes a Treebank tag and returns the corresponding WordNet tag.
	    """
	    if treebank_tag.startswith('J'):
	        return wordnet.ADJ
	    elif treebank_tag.startswith('V'):
	        return wordnet.VERB
	    elif treebank_tag.startswith('N'):
	        return wordnet.NOUN
	    elif treebank_tag.startswith('R'):
	        return wordnet.ADV
	    else:
	        return None


	def clean(self, string):
		"""
			Takes a string as argument and returns the same string with 
			non-letter characters replaced by white-space.
		"""
		return re.sub("[^a-zA-Z]", " ", string)


	def lemmatize(self, tokens):
		"""
			Lemmatize and turn lowercase. Takes a list of tokens, turns each
			token lowercase and lemmatizes the token. Returns a list of lemmas.
		"""
		lemmatizer = WordNetLemmatizer()
		wordnet_tagged_tokens = pos_tag(tokens)
		lemmatized_tokens = []
	    
		for token, tag in wordnet_tagged_tokens:
			wordnet_tag = self.get_wordnet_pos(tag)
			lower_token = token.lower()
			if lower_token not in self.stopwords and len(lower_token) > 1:
				if wordnet_tag is None:
					lemmatized_tokens.append(lower_token)
				else:
					lemmatized_tokens.append(lemmatizer.lemmatize(lower_token, pos=wordnet_tag))
	    
		return lemmatized_tokens


	def _configure_nltk_data_path(self):
		if self.nltk_data_path not in nltk.data.path:
			nltk.data.path.append(self.nltk_data_path.as_posix())













