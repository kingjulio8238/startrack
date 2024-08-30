# https://docs.multion.ai
# Make sure that the MultiOn Chrome Extension is installed and enabled (for more details, see here).

import os
import re
from multion.client import MultiOn
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class RepoData:
    name: str
    description: str
    num_stars: int

@dataclass
class StargazerData:
    user_id: str

@dataclass
class GitHubUserData:
    name: str
    num_followers: int
    location: str
    linkedin_url: Optional[str]
    twitter_url: Optional[str]
    email: Optional[str]

@dataclass
class LinkedInData:
    name: str
    location: str
    curr_job: str
    num_followers: int
    headline: str
    email: Optional[str]


class MultiOnUtils:
    def __init__(self, use_agentops: bool = False):
        self.multion_api_key = os.environ.get("MULTION_API_KEY")
        if not self.multion_api_key:
            raise ValueError("MULTION_API_KEY is not set in .env variables\nGet your API key from https://app.multion.ai/api-keys")
        if use_agentops:
            self.agentops_api_key = os.environ.get("AGENTOPS_API_KEY")
            if not self.agentops_api_key:
                raise ValueError("AGENTOPS_API_KEY is not set in .env variables\nGet your API key from https://app.agentops.ai/settings/projects")
        else:
            self.agentops_api_key=None

    def scrape_github(self, user = "areibman") -> GitHubUserData:
        client = MultiOn(api_key=self.multion_api_key, agentops_api_key=self.agentops_api_key)
        create_response = client.sessions.create(
            url=f"https://github.com/{user}",
            local=True,

        )
        print("scraping")

        session_id = create_response.session_id
        retrieve_response = client.retrieve(
            session_id=session_id,
            cmd="Get name, location, number of repositories, count of contributions in the last year, followers, following count, linkedin url, github url and email",
            fields=["name", "location", "public_repositories", "last_year_contributions_count",
                    "github_followers_count", "github_following_count", "linkedin_url", "github_url", "email"],
            scroll_to_bottom=False,
            render_js=True,
        )

        print(f"Raw data: {retrieve_response.data}")
        data = retrieve_response.data[0] if retrieve_response.data else {}

        # Extract email from raw data (sometimes scraper fetches prefixes or suffixes with an email)
        email_raw = data.get("email", "")
        if email_raw:
            email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', email_raw)
            email = email_match.group(0) if email_match else ""
        else:
            email = ""

        return GitHubUserData(
            name=data.get("name", ""),
            num_followers=int(data.get("github_followers_count", 0) or 0),
            location=data.get("location", ""),
            linkedin_url=data.get("linkedin_url"),
            twitter_url=data.get("twitter_url"),
            email=email,
        )

    def scrape_linkedin(self, link = "https://www.linkedin.com/in/alex-reibman-67951589") -> LinkedInData:
        client = MultiOn(api_key=self.multion_api_key, agentops_api_key=self.agentops_api_key)
        create_response = client.sessions.create(
            url="https://linkedin.com",
            local=True
        )

        session_id = create_response.session_id
        status = "CONTINUE"

        linkedin_url = f"{link}"

        while status == "CONTINUE":
            step_response = client.sessions.step(
                session_id=session_id,
                cmd=f"Go to {linkedin_url}"
            )
            status = step_response.status

        retrieve_response = client.retrieve(
            session_id=session_id,
            cmd="Get name, headline, location, current position, profile URL, number of followers and email",
            fields=["name", "headline", "location", "current_position", "profile_url", "num_followers", "email"],
            scroll_to_bottom=False,
            render_js=True,
            full_page=True,
            local=True
        )

        print(retrieve_response.data[0])
        data = retrieve_response.data[0] if retrieve_response.data else {}
        print(f"Raw LinkedIn data: {data}")

        return LinkedInData(
            name=data.get("name", ""),
            location=data.get("location", ""),
            curr_job=data.get("current_position", ""),
            num_followers=int(data.get("num_followers", 0) or 0),
            headline = data.get("headline", ""),
            email=data.get("email"),
        )

    def scrape_repo(self, repo_url: str) -> RepoData:
        client = MultiOn(api_key=self.multion_api_key, agentops_api_key=self.agentops_api_key)
        create_response = client.sessions.create(
            url=repo_url,
            local=True
        )

        session_id = create_response.session_id
        retrieve_response = client.retrieve(
            session_id=session_id,
            cmd="Get name, description and number of repo stars",
            fields=["name, description", "number_of_stars"],
            render_js=True,
            max_items=5
        )

        print(f"Raw data: {retrieve_response.data}")
        data = retrieve_response.data[0] if retrieve_response.data else {}

        # Extract numeric part and convert to int
        stars_str = data.get("number_of_stars", "0")
        num_stars = int(re.sub(r'[^0-9]', '', stars_str))

        return RepoData(
            name=data.get("name", ""),
            description=data.get("description", ""),
            num_stars=num_stars
        )

    def scrape_stargazers(self, repo_url: str) -> List[StargazerData]:
        client = MultiOn(api_key=self.multion_api_key)
        create_response = client.sessions.create(url=f"{repo_url}/stargazers", local=True)
        retrieve_response = client.retrieve(
            session_id=create_response.session_id,
            cmd="Get username for all users",
            fields=["username"],
            render_js=True,
            scroll_to_bottom=False,
            full_page=True,
            max_items=5
        )
        print(f"Stargazers scrape data: {retrieve_response.data}")
        stargazers = []
        if len(retrieve_response.data) > 0:
            stargazers = [StargazerData(user_id=user.get('username', '')) for user in retrieve_response.data]
        else:
            print("Did not scrape any users. Retry running the script or debug MultiOn retriever at:\nhttps://docs.multion.ai/api-reference/autonomous-api-reference/retrieve")
        print(f"Number of stargazers scraped: {len(stargazers)}")

        return stargazers

