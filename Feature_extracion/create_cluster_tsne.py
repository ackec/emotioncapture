import pandas as pd
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

# Read the CSV file
def read_csv(file_path):
    return pd.read_csv(file_path)

# Perform t-SNE clustering
def perform_tsne(data, perplexity=30, learning_rate=200, n_iter=1000):
    tsne = TSNE(n_components=2, perplexity=perplexity, learning_rate=learning_rate, n_iter=n_iter)
    tsne_result = tsne.fit_transform(data)
    return tsne_result

# Visualize the clustered data
def plot_clusters(tsne_result, labels):
    plt.scatter(tsne_result[:, 0], tsne_result[:, 1], c=labels, cmap='viridis', marker='o')
    plt.title('t-SNE Clustering')
    plt.xlabel('t-SNE Component 1')
    plt.ylabel('t-SNE Component 2')
    plt.show()

if __name__ == "__main__":
    # Replace 'your_data.csv' with the path to your CSV file
    csv_file_path = 'Feature_extracion/data.csv'
    
    # Read the CSV file
    data = read_csv(csv_file_path)

    # Assuming the last column contains the labels for clustering
    labels = data.iloc[:, -1]

    # Drop the labels column from the data
    data = data.iloc[:, :-1]

    # Perform t-SNE clustering
    tsne_result = perform_tsne(data)

    # Visualize the clustered data
    plot_clusters(tsne_result, labels)
