import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from collections import Counter

def analyze_starred_repos(input_filename, n_clusters=5):
    """
    Performs clustering analysis on starred GitHub repositories based on their topics
    and saves the results to a text file.

    Args:
        input_filename (str): Path to the JSON file containing starred repo data.
        n_clusters (int): The number of clusters to form.
    """
    try:
        # Load the data from the JSON file.
        with open(input_filename, 'r') as f:
            data = json.load(f)
        
        # We need to extract the repository information from the nested 'repo' key.
        repos = [item['repo'] for item in data]
        df = pd.DataFrame(repos)
        
        # Drop any rows where 'topics' is not a list or is empty.
        df['topics'] = df['topics'].apply(lambda x: x if isinstance(x, list) else [])
        df = df[df['topics'].str.len() > 0].reset_index(drop=True)
        
        if df.empty:
            print("No repositories with topics were found in the data. Clustering cannot be performed.")
            return

        # Join the list of topics into a single string for each repository.
        # This format is required for the TF-IDF Vectorizer.
        df['topics_str'] = df['topics'].apply(lambda x: " ".join(x))
        
        # --- Preprocessing and Vectorization ---
        # TF-IDF stands for Term Frequency-Inverse Document Frequency.
        # It's a numerical statistic that reflects the importance of a word in a document.
        # Here, each 'document' is a repository's list of topics.
        vectorizer = TfidfVectorizer(max_df=0.85, min_df=2)
        X = vectorizer.fit_transform(df['topics_str'])
        
        # --- K-Means Clustering ---
        # K-Means is an unsupervised learning algorithm that partitions data into k distinct, non-overlapping clusters.
        # It's ideal for this use case to find a high-level overview.
        kmeans_model = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=300, n_init=10, random_state=42)
        kmeans_model.fit(X)
        
        # Add the cluster label back to the DataFrame.
        df['cluster'] = kmeans_model.labels_
        
        # --- Analyzing the Clusters and Writing to File ---
        output_filename = f"clustering_analysis_{input_filename.split('_')[0]}.txt"

        with open(output_filename, 'w') as out_file:
            out_file.write(f"Clustering complete. Found {n_clusters} clusters:\n\n")
        
            # A mapping of feature indices to a list of feature names.
            feature_names = vectorizer.get_feature_names_out()
            
            # For each cluster, print the top topics and the repositories in it.
            for i in range(n_clusters):
                out_file.write(f"--- Cluster {i+1} ---\n")
                
                # Find the center of the cluster (the 'centroid').
                cluster_center = kmeans_model.cluster_centers_[i]
                
                # Get the top topics for this cluster by finding the highest TF-IDF scores.
                order_centroids = cluster_center.argsort()[::-1]
                top_topics = [feature_names[j] for j in order_centroids[:5]]  # Get top 5 topics
                
                # Find all repository names in this cluster.
                repos_in_cluster = df[df['cluster'] == i]['full_name'].tolist()
                
                out_file.write("Most common topics:\n")
                out_file.write("  " + ", ".join(top_topics) + "\n")
                
                out_file.write("\nRepositories in this cluster:\n")
                for repo_name in repos_in_cluster:
                    out_file.write(f"  - {repo_name}\n")
                out_file.write("\n" + "="*50 + "\n")

        print(f"Analysis successfully saved to '{output_filename}'")

    except FileNotFoundError:
        print(f"Error: The file '{input_filename}' was not found. Please run the previous script first to create it.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Get user input for the filename created by the previous script.
    username = input("Enter the GitHub username you used for the previous script: ")
    filename = f"{username}_starred_repos.json"
    
    # You can change the number of clusters here.
    num_clusters = int(input("How many clusters would you like to create (e.g., 5-10)? "))
    
    analyze_starred_repos(filename, num_clusters)
