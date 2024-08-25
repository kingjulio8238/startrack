import argparse
from dotenv import load_dotenv
from src.multion_utils import MultiOnUtils
from src.mem0_utils import MemorySystem
import csv

load_dotenv()

def main(repo_url, max_stargazers=None, scrape_linkedin=False, use_mem0=False, use_neo4j_kg=False):
    """
    Main function to scrape GitHub and LinkedIn data.
    """
    multion_scraper = MultiOnUtils()

    # Step 1: Scrape repo and stargazers
    print(f"Scraping repo: {repo_url}")
    repo = multion_scraper.scrape_repo(repo_url)
    print(f"Scraped repo: {repo}")

    print(f"Scraping stargazers: {repo}")
    stargazers = multion_scraper.scrape_stargazers(repo_url)
    if max_stargazers:
        stargazers = stargazers[:max_stargazers]
    print(f"Scraped {len(stargazers)} stargazers")

    # Step 2: Scrape GitHub data for each stargazer
    github_user_data = []
    for stargazer in stargazers:
        user_data = multion_scraper.scrape_github(stargazer.user_id)
        github_user_data.append(user_data)
    github_user_data = list({user.name: user for user in github_user_data}.values())
    print(f"Scraped GitHub data for {len(github_user_data)} users")

    # Step 3: Scrape LinkedIn data for users with LinkedIn URLs
    linkedin_data = {}
    if scrape_linkedin:
        for user in github_user_data:
            if user.linkedin_url:
                linkedin_profile = multion_scraper.scrape_linkedin(user.linkedin_url)
                if linkedin_profile.name:  # Only add if we got a valid name
                    linkedin_data[user.name] = linkedin_profile
    print(f"Scraped LinkedIn data for {len(linkedin_data)} users")

    # Step 4 Print or process the collected data as needed
    print("\nGitHub User Data:")
    for user in github_user_data:
        print(user)

    if scrape_linkedin:
        print("\nLinkedIn Data:")
        for name, profile in linkedin_data.items():
            print(f"{name}: {profile}")

    print("---\nScraping completed")


    # Step 4 Initialize Mem0 memory
    if use_mem0:
        memory_system = MemorySystem()
        memory = memory_system.get_memory()
        memory.reset()

        # Step 4a Memorize stargazers of each repository on a Knowledge Graph
        if use_neo4j_kg:
            repositories = [repo_url]
            # Iterate over the list of repositories

            for repository in repositories:
                print(f"Upserting repository: {repository}")

                # Iterate over the list of usernames for each repository
                for stargazer in stargazers:
                    print(f"  Upserting username: {stargazer.user_id}")

                    result = memory.add(f"The github user: {stargazer.user_id} starred the repository: {repository}", user_id=stargazer.user_id)

    # Step 5 Combine data and write to CSV
    print(f"Writing stargazers data to CSV. Number of GitHub users to write: {len(github_user_data)}")

    csv_filename = f"data/Stargazers_of_{repo.description.replace(' ', '_')[:30]}__.csv"
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        field_names = ['username', 'name', 'location', 'github_followers', 'linkedin_headline', 'current_position',
                      'linkedin_followers']
        writer = csv.DictWriter(csvfile, fieldnames=field_names)

        writer.writeheader()
        row_count = 0
        for user in github_user_data:
            try:
                linkedin_profile = linkedin_data.get(user.name)
                row = {
                    'username': user.name,
                    'name': linkedin_profile.name if linkedin_profile else user.name,
                    'location': linkedin_profile.location if linkedin_profile else (user.location or ''),
                    'github_followers': user.num_followers,
                    'linkedin_headline': getattr(linkedin_profile, 'headline', ''),
                    'current_position': getattr(linkedin_profile, 'curr_job', ''),
                    'linkedin_followers': getattr(linkedin_profile, 'num_followers', '')
                }
                writer.writerow(row)
                row_count += 1
                print(f"Writing row {row_count}: {row}")
            except Exception as e:
                print(f"Error writing CSV row for user: {user.name}: {str(e)}")

    print(f"---\nTotal rows written to {csv_filename}: {row_count}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape GitHub and LinkedIn data for repository stargazers.")
    parser.add_argument("repo_url", help="URL of the GitHub repository to scrape")
    parser.add_argument("--max-stargazers", type=int, help="Maximum number of stargazers to scrape")
    parser.add_argument("--with-linkedin", action="store_true", default=False,
                        help="Scrape LinkedIn profiles")
    parser.add_argument("--with-mem0", action="store_true", default=False,
                        help="Option to include memory usage for scraping")
    parser.add_argument("--with-neo4j-kg", action="store_true", default=False,
                        help="Option to use Neo4j knowledge graph")

    args = parser.parse_args()

    main(args.repo_url, args.max_stargazers, args.with_linkedin, args.with_mem0, args.with_neo4j_kg)