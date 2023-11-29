from sklearn.datasets import fetch_openml
from sklearn.decomposition import PCA
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Dimension reduction and clustering libraries
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


def cluster_keypoints(keypoints_csv):
    data = pd.read_csv(keypoints_csv)

    standard_embedding = umap.UMAP(random_state=10).fit_transform(data.values)

    cmap = ['red', 'blue', 'green']
    kmeans_labels = cluster.KMeans(n_clusters=3).fit_predict(data)
    #print(kmeans_labels)
    clustered = (kmeans_labels >= 0)
    s1 = plt.scatter(standard_embedding[:, 0], standard_embedding[:, 1], c=[cmap[label] for label in kmeans_labels[clustered]], s=10)

    labels = kmeans_labels
    color_array = np.where(abs(labels) == 0, "red", labels)
    color_array = np.where(abs(labels) == 1, "blue", color_array)
    color_array = np.where(abs(labels) == 2, "green", color_array)

        #print(s2)


    print(color_array)

    df = pd.DataFrame(color_array.T)
    headers_to_csv = ['color']
    df.to_csv('color_array_kmeans.csv', header=headers_to_csv, index=False)

    labels = kmeans_labels
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    #n_noise_ = list(labels).count(-1)

    print("Estimated number of clusters: %d" % n_clusters_)

    #plt.legend(s1.legend_elements()[0], list(set(kmeans_labels)))
    plt.title('K-means clustering', fontsize=20)
    plt.xlabel('UMAP_1')
    plt.show()


if __name__ == "__main__":
    cluster_keypoints("data.csv")
