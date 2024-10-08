import argparse
from dotenv import load_dotenv

from src.mailchimp_adapter import MailchimpAdapter
from src.multion_utils import MultiOnUtils
from src.mem0_utils import MemorySystem
from src.time_utils import Time
import csv
import os

load_dotenv()

def main(
        repo_url,
        max_stargazers=None,
        scrape_linkedin=False,
        use_agentops=False,
        use_mem0=False,
        use_neo4j_kg=False,
        use_mailchimp=False
    ):
    """
    Main function to scrape GitHub and LinkedIn data.

    This function takes in a GitHub repository URL and several optional parameters:
    max_stargazers: Maximum number of stargazers to scrape
    scrape_linkedin: Whether to scrape LinkedIn profiles
    use_mem0: Whether to use Mem0 memory system
    use_neo4j_kg: Whether to use Neo4j knowledge graph
    The function scrapes the repository and its stargazers, then scrapes GitHub data for each stargazer. If scrape_linkedin is True, it also scrapes LinkedIn data for users with LinkedIn URLs. The function then writes the collected data to a CSV file.

    It prints various debugging messages throughout its execution.
    """
    multion_scraper = MultiOnUtils(use_agentops=use_agentops)
    if use_mailchimp == True:
        mailchimp_adapter = MailchimpAdapter()
    agent_name = "StarTracker"

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
    if scrape_linkedin == True:
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

    if scrape_linkedin == True:
        print("\nLinkedIn Data:")
        for name, profile in linkedin_data.items():
            print(f"{name}: {profile}")

    print("---\nScraping completed")


    # Step 4 Initialize Mem0 memory
    if use_mem0 == True:
        memory_system = MemorySystem()
        memory = memory_system.get_memory()
        # memory.reset()

        # Step 4a Memorize stargazers of each repository on a Knowledge Graph
        if use_neo4j_kg == True:
            print(f"Updating knowledge graph")
            repositories = [repo_url]
            # Iterate over the list of repositories

            for repository in repositories:
                print(f"Upserting repository: {repository}")
                result_repository = memory.add(
                    f"The github user: {stargazer.user_id} starred the repository: {repository}",
                    user_id=None,
                    agent_id=agent_name,
                    run_id=str(Time()),
                    metadata={'app_id': repository},
                )

                # Iterate over the list of usernames for each repository
                for stargazer in stargazers:
                    print(f"  Upserting username: {stargazer.user_id}")

                    result_stargazer = memory.add(
                        f"The github user: {stargazer.user_id} starred the repository: {repository}",
                        user_id=stargazer.user_id,
                        agent_id=agent_name,
                        run_id=str(Time()),
                        metadata={'app_id': repository},
                    )

    # Step 5 Combine data and write to CSV
    print(f"Writing stargazers data to CSV. Number of GitHub users to write: {len(github_user_data)}")
    # Create the 'data' directory if it doesn't exist
    os.makedirs('data', exist_ok=True)

    csv_filename = f"data/Stargazers_of_{repo.description.replace(' ', '_')[:30]}__{str(Time())}.csv"
    print(f"Saved file: {csv_filename}")
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        field_names = ['username', 'email', 'name', 'location', 'github_followers', 'linkedin_headline', 'current_position',
                      'linkedin_followers']
        writer = csv.DictWriter(csvfile, fieldnames=field_names)

        writer.writeheader()
        row_count = 0
        for user in github_user_data:
            try:
                linkedin_profile = linkedin_data.get(user.name)
                row = {
                    'username': user.name,
                    'email': user.email or (linkedin_profile.email if linkedin_profile else '') or '',
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

    # Step 6 Add emails to mailchimp list
    if use_mailchimp == True:
        print(f"Adding emails to Mailchimp list")
        scraped_emails = [user.email for user in github_user_data if user.email]
        tag_name = repo.name

        if scraped_emails:
            print(f"Processing {len(scraped_emails)} emails")
            mailchimp_adapter.process_emails(scraped_emails, f"tag_{tag_name}")
        else:
            print("No emails found to process")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape GitHub and LinkedIn data for repository stargazers.")
    parser.add_argument("repo_url", help="URL of the GitHub repository to scrape")
    parser.add_argument("-limit","--max-stargazers", type=int, help="Maximum number of stargazers to scrape")
    parser.add_argument("-li","--with-linkedin", action="store_true", default=False,
                        help="Scrape LinkedIn profiles")
    parser.add_argument("-aops","--with-agentops", action="store_true", default=False,
                        help="Use Agentops for tracking and reporting agents' actions")
    parser.add_argument("-mem0", "--with-mem0", action="store_true", default=False,
                        help="Option to include memory usage for scraping")
    parser.add_argument("-mailchimp", "--with-mailchimp", action="store_true", default=False,
                        help="Option to include adding scraped users to mailchimp list")
    parser.add_argument("-kg", "--with-neo4j-kg", action="store_true", default=False,
                        help="Option to use Neo4j knowledge graph. Requires --with-mem0")

    args = parser.parse_args()
    if args.with_neo4j_kg and not args.with_mem0:
        parser.error("--with-neo4j-kg requires --with-mem0 to be present")

    main(args.repo_url, args.max_stargazers, args.with_linkedin, args.with_agentops, args.with_mem0, args.with_neo4j_kg, args.with_mailchimp)
