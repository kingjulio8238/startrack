import argparse
from dotenv import load_dotenv
from multion_utils import MultiOnUtils
from mem0_utils import MemorySystem

load_dotenv()

def main(repo_url, max_stargazers=None, scrape_linkedin=True):
    """
    Main function to scrape GitHub and LinkedIn data.
    """
    multionscrapper = MultiOnUtils()
    
    # Step 1: Scrape repo and stargazers
    repo = multionscrapper.scrape_repo(repo_url)
    print(f"Repo: {repo}")
    stargazers = multionscrapper.scrape_stargazers(repo_url)
    if max_stargazers:
        stargazers = stargazers[:max_stargazers]
    print(f"Scraped {len(stargazers)} stargazers")
    
    # Step 2: Scrape GitHub data for each stargazer
    github_user_data = []
    for stargazer in stargazers:
        user_data = multionscrapper.scrape_github(stargazer.user_id)
        github_user_data.append(user_data)
    print(f"Scraped GitHub data for {len(github_user_data)} users")
    
    # Step 3: Scrape LinkedIn data for users with LinkedIn URLs
    linkedin_data = []
    if scrape_linkedin:
        for user in github_user_data:
            if user.linkedin_url:
                linkedin_profile = multionscrapper.scrape_linkedin(user.linkedin_url)
                linkedin_data.append(linkedin_profile)
        print(f"Scraped LinkedIn data for {len(linkedin_data)} users")
    
    # Print or process the collected data as needed
    print("\nGitHub User Data:")
    for user in github_user_data:
        print(user)
    
    if scrape_linkedin:
        print("\nLinkedIn Data:")
        for profile in linkedin_data:
            print(profile)
    
    print("\nScraping completed")


    """
    Initialize GraphMemory
    """
    memory_system = MemorySystem()
    memory = memory_system.get_memory()

    """
    Memorize stargazers of each repository
    """
    repositories = ["mem0ai/mem0", "MULTI-ON/multion-python"]
    usernames = ["userA", "userB"]
    # Iterate over the list of repositories

    for repository in repositories:
        print(f"Repository: {repository}")
        # Iterate over the list of usernames for each repository
        for username in usernames:
            print(f"  Username: {username}")
            result = memory.add(f"The github user: {username} starred the repository: {repository}", user_id=username)

    # Combine data and write to CSV
    csv_filename = f"{repo.description.replace(' ', '_')[:30]}_users.csv"
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['username', 'name', 'location', 'github_followers', 'linkedin_headline', 'current_position', 'linkedin_followers']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for user in github_user_data:
            linkedin_profile = linkedin_data.get(user.name, {})
            row = {
                'username': user.name,
                'name': linkedin_profile.get('name', user.name),
                'location': linkedin_profile.get('location') or user.location or None,
                'github_followers': user.num_followers,
                'linkedin_headline': linkedin_profile.get('headline', None),
                'current_position': linkedin_profile.get('current_position', None),
                'linkedin_followers': linkedin_profile.get('num_followers', None)
            }
            writer.writerow(row)
    
    print(f"\nData written to {csv_filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape GitHub and LinkedIn data for repository stargazers.")
    parser.add_argument("repo_url", help="URL of the GitHub repository to scrape")
    parser.add_argument("--max-stargazers", type=int, help="Maximum number of stargazers to scrape")
    parser.add_argument("--no-linkedin", action="store_true", help="Skip LinkedIn scraping")
    
    args = parser.parse_args()
    
    main(args.repo_url, args.max_stargazers, not args.no_linkedin)
