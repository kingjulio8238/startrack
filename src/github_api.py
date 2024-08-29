import argparse
from dotenv import load_dotenv
import requests
import time
from pydantic import BaseModel
from typing import List, Optional

load_dotenv()

class UserDetails(BaseModel):
    name: Optional[str]
    location: Optional[str]
    company: Optional[str]
    followers: Optional[int]
    username: str
    twitter: Optional[str]
    linkedin: Optional[str]
    email: Optional[str]

def get_user_details(username):
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    # Get user details
    user_url = f"https://api.github.com/users/{username}"
    user_response = requests.get(user_url, headers=headers)
    if user_response.status_code != 200:
        print(f"Error fetching user details for {username}: {user_response.status_code}")
        return None
    
    user_data = user_response.json()
    
    # Get social accounts
    social_url = f"https://api.github.com/users/{username}/social_accounts"
    social_response = requests.get(social_url, headers=headers)
    social_accounts = social_response.json() if social_response.status_code == 200 else []
    
    linkedin = next((account['url'] for account in social_accounts if account['provider'] == 'linkedin'), None)
    
    return UserDetails(
        name=user_data.get('name'),
        location=user_data.get('location'),
        email=user_data.get('email'),
        company=user_data.get('company'),
        followers=user_data.get('followers'),
        username=username,
        twitter=user_data.get('twitter_username'),
        linkedin=linkedin
    )

def get_stargazers(owner: str, repo: str, max_users: Optional[int] = None) -> List[UserDetails]:
    base_url = f"https://api.github.com/repos/{owner}/{repo}/stargazers"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    params = {"per_page": 100, "page": 1}
    all_stargazers = []

    while True:
        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.json())
            break

        stargazers_page = response.json()
        if not stargazers_page:
            break

        for stargazer in stargazers_page:
            user_details = get_user_details(stargazer['login'])
            if user_details:
                all_stargazers.append(user_details)
                print(f"Fetched details for {user_details.username}")

            if max_users and len(all_stargazers) >= max_users:
                return all_stargazers

        print(f"Fetched page {params['page']}, total stargazers: {len(all_stargazers)}")

        if 'next' not in response.links:
            break

        params['page'] += 1
        
        # Respect GitHub's rate limit
        time.sleep(2)

    return all_stargazers