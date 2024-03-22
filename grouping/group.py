import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import DBSCAN
from sklearn.model_selection import ParameterGrid
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (
	silhouette_score, calinski_harabasz_score, davies_bouldin_score
	)

from data_manager.manager import DataManager
from grouping.preprocess import Preprocess
from config.settings import parameter_grid

class Group:
	"""
		Class responsible for grouping articles based on similarity. It uses
		sklearn's TfidfVectorizer. the vectorizer is fitted to a 
		combination of archived and current articles for better results. The 
		proccessed text of current articles are transformed into a spare matrix.
		It reduces the dimensionality of the sparse matrix using sklearn's
		TruncatedSVD. It uses sklearn's DBSCAN to detect clusters. A custom 
		parameter search is used to to find the best values for 'eps' (the 
		distance parameter for DBSCAN )and 'n_components' (the number of 
		desired dimensions for TruncatedSVD). To find the 'best' set of params.
		we have a custom function that combines the weighted silhouette, 
		Calinski-Harabasz and inverse Davies-Boulding scores with higher scores
		meaning better fit. Furthermore, we prefer  parameters that produce
		higher number of clusters. The second condition ensures that the 
		composite scoring doesn't produce large blobs of unrelated articles.

		Attributes:
			manager (obj): data manager object
			current (list): list of current articles
			archived (list): list of archived articles
			combined (list): list of current + archived
	"""
	def __init__(self, param_grid=parameter_grid):
		"""
			Initialise class attributes

			Params:
				param_grid (dict): parameter grid used in 'param_search' default
				is loaded from 'config/settings.py'. Dict is {"eps": [ints],
				"n_components": [ints]}
		"""
		self.manager = DataManager()
		self.current = self.manager.load()
		self.archived = self.manager.load("archived")
		self.combined = self.current + self.archived
		self.vectorizer = self.fit_vectorizer()
		self.tfidf_matrix = self.transform_with_vectorizer()
		self.param_grid = param_grid
		self.best_svd = None
		self.best_dbscan = None
		self.group_labels = None


	def group(self):
		"""
			Main method that automatically groups the current articles and adds 
			the groups to the article dictionaries then saves them.
		"""
		# Performing param search if it wasnt done yet
		if not self.best_svd:
			self.param_search()

		# Adding group labels to article dictionaries
		for label, article in zip(self.group_labels, self.current):
			article["group"] = int(label)

		# Saving current articles with group labels
		self.manager.save(self.current, "articles")

	def param_search(self):
		"""
			Custom parameter search method. Iterates over each combination of 
			parameters, for each combination the models are trained and 
			evaluated using 'composite_score' prefering higher number of 
			clusters. It uses Sklearn's ParameterGrid to retrieve the possible
			combinations. The best parameters, models and associated cluster 
			labels are stored as class attributes 'best_svd', 'best_dbscan' and 
			'group_labels'.
		"""
		# Initialising trackers
		best_score = -1
		best_params = None
		best_n_clusters = 0
		best_TruncSVD = None
		best_DBSCAN = None

		# Iterating over parameter combinations
		for parameters in ParameterGrid(self.param_grid):
			# Unpacking parameters
			comps = parameters["n_components"]
			eps = parameters["eps"]

			# Fitting TruncatedSVD with parameters
			svd = TruncatedSVD(n_components=comps, random_state=42)
			# Transforming the tfidf matrix
			reduced_tfidf_matrix = svd.fit_transform(self.tfidf_matrix)

			# Fitting the DBSCAN with parameters
			dbscan = DBSCAN(eps=eps, min_samples=2, metric="cosine")
			dbscan.fit(reduced_tfidf_matrix)

			# Computing number of clusters
			c_labels = dbscan.labels_
			n_clusters = len(set(c_labels))

			# Evaluating parameters
			if n_clusters > 1:
				s = silhouette_score(reduced_tfidf_matrix, c_labels)
				ch = calinski_harabasz_score(reduced_tfidf_matrix, c_labels)
				db = davies_bouldin_score(reduced_tfidf_matrix, c_labels)
				score = self.composite_score(s, ch, db)
				if score > best_score and n_clusters > best_n_clusters:
					best_n_clusters = n_clusters
					best_score = score
					best_params = parameters
					self.best_dbscan = dbscan
					self.best_svd = svd
					self.group_labels = c_labels


	def composite_score(self, s, ch, db):
		"""
			Method that combines the silhouette, Calinski-Harabasz and 
			inverse Davies-Boulding scores. The combination is equally weighted.

			Params:
				s (float): shilouette score
				ch (float): Calinski-Harabasz score
				db (flaot): Davies-Boulding score
			Returns:
				composite (float): combined score
		"""
		# Inverting db score
		db_inverse = 1 / (1 + db)

		# Vectorising scores and weights
		scores = np.array([s, ch, db_inverse])
		weights = np.array([1/3, 1/3, 1/3])

		# Combining scores 
		composite = np.dot(scores, weights)

		return composite


	def transform_with_vectorizer(self):
		"""
			Method transforms the processed texts of current articles.
			
			Returns:
				tfidf_matrix (obj): scipy sparse matrix, each row is an article
				each column is tfidf transformed token.
		"""
		tfidf_matrix = self.vectorizer.transform(
			[article["processed_text"] for article in self.current]
			)
		return tfidf_matrix


	def fit_vectorizer(self):
		"""
			Method fits TfidfVectoriser to the processed texts of the combined
			articles.

			Returns:
				vectorizer (obj): sklearn transformer object
		"""
		vectorizer = TfidfVectorizer()
		vectorizer.fit([article["processed_text"] for article in self.combined])
		return vectorizer





