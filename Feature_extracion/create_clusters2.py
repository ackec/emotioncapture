from sklearn.datasets import fetch_openml
from sklearn.decomposition import PCA
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Dimension reduction and clustering libraries
import umap
import hdbscan
import sklearn.cluster as cluster
from sklearn.metrics import adjusted_rand_score, adjusted_mutual_info_score

data = pd.read_csv("data.csv")

mnist = fetch_openml('mnist_784', version=1)
mnist.target = mnist.target.astype(int)


standard_embedding = umap.UMAP(random_state=10).fit_transform(data.values)
lowd_data = PCA(n_components=1).fit_transform(data.values)
hdbscan_labels = hdbscan.HDBSCAN(min_samples=10, min_cluster_size=12).fit_predict(standard_embedding)

cmap = ['red', 'blue', 'green', 'pink', 'purple', 'orange', 'brown', 'teal']
clustered = (hdbscan_labels >= 0)
#s1 = plt.scatter(standard_embedding[~clustered, 0], standard_embedding[~clustered, 1], color=(0.5, 0.5, 0.5), s=10, alpha=0.5)
s2 = plt.scatter(standard_embedding[clustered, 0], standard_embedding[clustered, 1], c=[cmap[label] for label in hdbscan_labels[clustered]], s=10)

#print(s2)
labels = hdbscan_labels

color_array = np.where(abs(labels) == 0, "red", labels)
color_array = np.where(abs(labels) == 1, "blue", color_array)
color_array = np.where(abs(labels) == 2, "green", color_array)
color_array = np.where(abs(labels) == 3, "pink", color_array)
color_array = np.where(abs(labels) == 4, "purple", color_array)
color_array = np.where(abs(labels) == 5, "orange", color_array)
color_array = np.where(abs(labels) == 6, "brown", color_array)
color_array = np.where(abs(labels) == 7, "teal", color_array)

print(color_array)

df = pd.DataFrame(color_array.T)
headers_to_csv = ['color']
df.to_csv('color_array.csv', header=headers_to_csv, index=False)

set(hdbscan_labels)
Counter(hdbscan_labels)

labels = hdbscan_labels
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
#n_noise_ = list(labels).count(-1)

print("Estimated number of clusters: %d" % n_clusters_)
#print("Estimated number of noise points: %d" % n_noise_)

plt.legend(s2.legend_elements()[0], list(set(cmap)))
plt.title('UMAP clustering of 457 images', fontsize=20)
plt.xlabel('UMAP_1')
plt.ylabel('UMAP_2')
plt.show()