# https://docs.multion.ai
# Make sure that the MultiOn Chrome Extension is installed and enabled (for more details, see here).

import os
from multion.client import MultiOn
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class RepoData:
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

@dataclass
class LinkedInData:
    name: str
    location: str
    curr_job: str
    num_followers: int

class MultiOnUtils:
    def __init__(self):
        self.multion_api_key = os.environ.get(
            "MULTION_API_KEY")  # Get your API key from https://app.multion.ai/api-keys
        self.agentops_api_key = os.environ.get(
            "AGENTOPS_API_KEY")  # Get your API key from https://app.agentops.ai/settings/projects
        if not self.multion_api_key:
            raise ValueError("MULTION_API_KEY is not set in .env variables")

    def scrape_github(self, user = "areibman") -> RepoData:
        client = MultiOn(api_key=self.multion_api_key)
        # client = MultiOn(api_key=self.multion_api_key, agentops_api_key=self.agentops_api_key)
        create_response = client.sessions.create(
            url=f"https://github.com/{user}",
            local=True
        )
        print("scraping")

        session_id = create_response.session_id
        retrieve_response = client.retrieve(
            session_id=session_id,
            cmd="Get name, location, number of repositories, count of contributions in the last year, followers and following count.",
            fields=["name", "location", "public_repositories", "last_year_contributions_count",
                    "github_followers_count", "github_following_count"],
            scroll_to_bottom=False,
            render_js=True
        )

        print(retrieve_response.data)
        data = retrieve_response.data

        return data

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
            cmd="Get name, headline, location, current position, profile URL, and image URL.",
            fields=["name", "headline", "location", "current_position", "profile_url", "image_url"],
            scroll_to_bottom=True,
            render_js=True
        )

        print(retrieve_response.data[0])
        data = retrieve_response.data[0]

        return data

    def scrape_repo(self, repo_url: str) -> RepoData:
        # TODO: Implement MultiOn scraping logic
        # This method should return a RepoData object
        pass

    def scrape_stargazers(self, repo_url: str) -> List[StargazerData]:
        # TODO: Implement MultiOn scraping logic
        # This method should return a list of StargazerData objects
        pass

