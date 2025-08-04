import requests
import json
import os

def get_starred_repositories(username, pat):
    """
    Fetches all starred repositories for a given GitHub user using pagination.

    Args:
        username (str): The GitHub username.
        pat (str): A GitHub Personal Access Token with 'repo' scope.

    Returns:
        list: A list of dictionaries, where each dictionary represents a starred repository.
              Returns an empty list if an error occurs.
    """
    # Base URL for the GitHub API endpoint for a user's starred repositories.
    url = f"https://api.github.com/users/{username}/starred"
    
    # Headers for the API request.
    # The Authorization header is required for a higher rate limit.
    # We use a custom media type to get the 'starred_at' timestamp.
    headers = {
        "Authorization": f"token {pat}",
        "Accept": "application/vnd.github.v3.star+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    
    starred_repos = []
    
    try:
        while url:
            # Make the GET request to the GitHub API.
            print(f"Fetching from: {url}")
            response = requests.get(url, headers=headers)
            
            # Check for a successful response (status code 200).
            response.raise_for_status()
            
            # Append the repositories from the current page to our list.
            starred_repos.extend(response.json())
            
            # Get the 'Link' header for pagination.
            # The 'Link' header tells us if there is a next page.
            link_header = response.headers.get('Link')
            
            # If there's a 'Link' header, parse it to find the URL for the next page.
            if link_header:
                links = requests.utils.parse_header_links(link_header)
                next_page_url = None
                for link in links:
                    if link.get('rel') == 'next':
                        next_page_url = link.get('url')
                        break
                
                # Update the URL for the next iteration of the loop.
                # If there's no 'next' link, the loop will terminate.
                url = next_page_url
            else:
                # If no 'Link' header, we've reached the end.
                url = None
                
        return starred_repos
        
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
    return []

if __name__ == "__main__":
    # Get user input for GitHub username and Personal Access Token (PAT).
    github_username = input("Enter your GitHub username: ")
    github_pat = input("Enter your GitHub Personal Access Token: ")

    if not github_username or not github_pat:
        print("Username and PAT are required.")
    else:
        # Call the function to fetch the starred repos.
        repos = get_starred_repositories(github_username, github_pat)

        if repos:
            print(f"\nFound {len(repos)} starred repositories for user '{github_username}':\n")
            
            # Print a summary for each repository.
            for repo_data in repos:
                repo_info = repo_data.get('repo', {})
                name = repo_info.get('full_name', 'N/A')
                language = repo_info.get('language', 'N/A')
                stars = repo_info.get('stargazers_count', 'N/A')
                starred_at = repo_data.get('starred_at', 'N/A')
                
                print(f"  - {name}")
                print(f"    Language: {language}")
                print(f"    Stars: {stars}")
                print(f"    Starred At: {starred_at}\n")
            
            # Optional: Save the data to a JSON file.
            output_filename = f"{github_username}_starred_repos.json"
            with open(output_filename, 'w') as f:
                json.dump(repos, f, indent=4)
            print(f"All data has been saved to '{output_filename}'")
            
        else:
            print("No repositories found or an error occurred. Please check your username and PAT.")
