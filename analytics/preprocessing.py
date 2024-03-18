import re

# NLTK Imports
import nltk
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


class PreprocessArticleText:
	stopwords = set(stopwords.words('english'))

	def __init__(self, datadict):
		self.datadict = datadict


	def get_full_text(self):
		"""
			Extract body, headline and description
		"""

	@staticmethod
	def get_wordnet_pos(treebank_tag):
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


	def clean(self, text):
		"""
			Replaces all non-letter characters with whitespace. Param is single
			(str).
		"""
		return re.sub("[^a-zA-Z]", " ", text)


	def tokenize(self, text):
		return nltk.word_tokenize(text)


	def lemmatize(self, tokens):
		"""
			Lemmatize and turn lowercase. Takes (list) tokens, returns (list) 
			lemmas.
		"""
		lemmatizer = WordNetLemmatizer()
		wordnet_tagged_tokens = nltk.pos_tag(tokens)
		lemmatized_tokens = []
	    
		for token, tag in wordnet_tagged_tokens:
			wordnet_tag = Preprocess.get_wordnet_pos(tag)
			lower_token = token.lower()
			if lower_token not in Preprocess.stopwords and len(lower_token) > 1:
				if wordnet_tag is None:
					lemmatized_tokens.append(lower_token)
				else:
					lemmatized_tokens.append(lemmatizer.lemmatize(lower_token, pos=wordnet_tag))
	    
		return lemmatized_tokens


	def process(self, text_lst):
		"""
			Preprocessing function, cleans, tokenizes, lematizes and finally
			merges the lemmas into a single string. 
			Takes (list) of strings as input, returns a processed (list) of 
			strings.
		"""
		processed_text = []
		for text in text_lst:
			clean_lst = self.clean(text)
			tokens_lst = nltk.word_tokenize(clean_lst)
			lemma_lst = self.lemmatize(tokens_lst)
			merged = " ".join(lemma_lst)
			processed_text.append(merged)
		return processed_text












