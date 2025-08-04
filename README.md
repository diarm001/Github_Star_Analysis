Starred GitHub Repo Analysis

Ever wonder what patterns lie within your GitHub stars? This project is a simple but powerful tool to automatically fetch and analyze your starred repositories, revealing your core interests and tech focus through clustering.

Turn a long list of repositories into a clear, high-level overview of your development habits.

✨ Features
Automated Data Collection: Fetches your complete list of starred repositories from the GitHub API, handling pagination automatically.

Intelligent Clustering: Uses machine learning to group repositories into distinct clusters based on their topics.

Insightful Output: Generates a clean text file outlining each cluster, its most common topics, and the repositories within it.

🚀 Getting Started
Prerequisites

You'll need Python 3 and a few libraries to run these scripts. You can install them with pip:

pip install requests pandas scikit-learn

You also need a GitHub Personal Access Token (PAT) with the public_repo scope.

Step 1: Gather Your Data

First, run the data collection script to fetch your starred repos. It will prompt you for your GitHub username and PAT.

python get_starred_repos.py

This will create a YOUR_USERNAME_starred_repos.json file in your directory.

Step 2: Analyze and Cluster

Next, run the analysis script. It will read your JSON file, perform the clustering, and output the results to a text file.

python cluster_repos.py

The script will ask you how many clusters you'd like to create (e.g., 5-10). The final output will be saved to clustering_analysis_YOUR_USERNAME.txt.

Example Output

Here's a glimpse of what the analysis looks like:

Clustering complete. Found 10 clusters:

--- Cluster 1 ---
Most common topics:
  rust, webassembly, kafka, cryptography, emscripten

Repositories in this cluster:
  - alexpasmantier/television
  - prefix-dev/pixi
  - gosub-io/gosub-engine
  ...

🧠 Insights
The clusters reveal your primary areas of interest. You can use this analysis to:

Identify Your Niche: Confirm your focus in areas like AI, data science, or web development.

Discover Connections: Find unexpected links between different projects you've starred.

Plan Your Learning: Use the clusters as a guide for what topics to explore next.

This is just the start—the raw JSON data is a goldmine for even deeper analysis!
