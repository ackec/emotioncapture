import numpy as np
from sklearn.datasets import fetch_openml
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import pandas as pd

from sklearn import metrics
from sklearn.cluster import DBSCAN
from collections import Counter
import sklearn.cluster as cluster

import hdbscan
import random
import umap

data = pd.read_csv("data.csv")
#seed =np.seed(1337)

embedding = umap.UMAP(random_state=42).fit_transform(data.values)

get_clusters = DBSCAN(eps = 0.5, min_samples = 10).fit_predict(embedding)
# eps
# The maximum distance between two samples for one to be 
# considered as in the neighborhood of the other. 
# This is not a maximum bound on the distances of points within a cluster. 
# This is the most important DBSCAN parameter to choose appropriately for your data set and distance function.
#
# min_samples
# The number of samples (or total weight) in a neighborhood for a point to be considered as a core point. 
# This includes the point itself. If min_samples is set to a higher value, DBSCAN will find denser clusters, 
# whereas if it is set to a lower value, the found clusters will be more sparse.
#
#Noisy samples are given the sample -1


set(get_clusters)
Counter(get_clusters)

s1 = plt.scatter(embedding[:, 0], embedding[:, 1], c = get_clusters, cmap = 'viridis')

# k_means
standard_embedding = umap.UMAP(random_state=42).fit_transform(data.values)
kmeans_labels = cluster.KMeans(n_clusters=10).fit_predict(data)
#s2 = plt.scatter(standard_embedding[:, 0], standard_embedding[:, 1], c=kmeans_labels, s=10, cmap='Spectral')

set(kmeans_labels)
Counter(kmeans_labels)

#print(get_clusters == 2)
labels2 = kmeans_labels
labels1 = get_clusters
n_clusters_ = len(set(labels1)) - (1 if -1 in labels1 else 0)
n_noise_ = list(labels1).count(-1)

print("Estimated number of clusters: %d" % n_clusters_)
print("Estimated number of noise points: %d" % n_noise_)

plt.legend(s1.legend_elements()[0], list(set(labels1)))
plt.title('UMAP clustering of 457 images', fontsize=20)
plt.xlabel('UMAP_1')
plt.ylabel('UMAP_2')
plt.show()