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
    standard_embedding = data[["umap_x", "umap_y"]].values
    # values = data[['eye_opening', 'ear_opening', 'ear_angle', 'ear_pos_vec', 'snout_pos', 'mouth_pos', 'face_incl']].values
    hdbscan_labels = hdbscan.HDBSCAN(min_samples=10, min_cluster_size=12).fit_predict(standard_embedding)
    kmeans_labels = cluster.KMeans(n_clusters=3).fit_predict(standard_embedding)

    cmap = ['red', 'blue', 'green', 'pink', 'purple', 'orange', 'brown', 'teal', 'darkgreen', 'chocolate', 'cyan']
    clustered = (hdbscan_labels >= 0)
    clustered_kmeans = (kmeans_labels >= 0)
    #s2 = plt.scatter(standard_embedding[clustered, 0], standard_embedding[clustered, 1], c=[cmap[label] for label in hdbscan_labels[clustered]], s=10)
    s3 = plt.scatter(standard_embedding[clustered_kmeans, 0], standard_embedding[clustered_kmeans, 1], c=[cmap[label] for label in kmeans_labels[clustered_kmeans]], s=10)

    labels = hdbscan_labels
    color_array = np.where(abs(labels) == 0, "red", labels)
    amount_of_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    xlabel = "Amount of clusters:" + str(amount_of_clusters)
    xlabel = "Amount of clusters:" + str(3)

    if len(cmap) > 10:
        print("Too many clusters! Modify parameters or dataset.")
        amount_of_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    for i in range(0, len(cmap)): 
        color_array = np.where(abs(labels) == i, cmap[i], color_array)
       
    print(color_array)

    df = pd.DataFrame(color_array.T)
    headers_to_csv = ['color']
    df.to_csv('color_array.csv', header=headers_to_csv, index=False)

    set(hdbscan_labels)
    Counter(hdbscan_labels)

    labels = hdbscan_labels

    plt.title('K-means', fontsize=20)
    plt.xlabel(xlabel)
    plt.show()


if __name__ == "__main__":
    # do_umap_projection("output/mouse_features.csv")
    cluster_keypoints("output/mouse_features.csv")
