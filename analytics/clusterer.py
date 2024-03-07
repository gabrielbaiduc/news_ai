from data_manager.manager import load_data
import pandas as pd

data = load_data()

outdated_link = data.pop("outdated_links")

articles = pd.DataFrame(data)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN

# Vectorize the text using TF-IDF
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(articles["text"])

# Perform DBSCAN clustering
dbscan = DBSCAN(eps=0.9, min_samples=2)  # You may need to adjust these parameters
dbscan.fit(tfidf_matrix)

# Get cluster labels
cluster_labels = dbscan.labels_

# Attach cluster labels
articles["cluster"] = cluster_labels

for i in range(max(cluster_labels)+1):
	print(i)
	print(articles.loc[cluster_labels == i]["title"])
	print(articles.loc[cluster_labels == i]["source"])
	print(articles.loc[cluster_labels == i]["category"])
