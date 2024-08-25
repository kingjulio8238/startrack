from dotenv import load_dotenv
from multion_utils import MultiOnUtils

load_dotenv()

def main():
    """
        Step 1 user input
        Agent role: Listen to the user intent and preferences
        Tools: MultiOn, AgentOps, Mem0

        1. We receive an intent prompt from a user
        2. We assume a use case where the user wants to learn about github repositories and their users, and user profiles
        3. We use MultiOn to access private (behind auth) data of the human-in-control user
        4. Multi on pulls data from intended sources, like Github, LinkedIn, ...
        5. We store accessed data/memories in Python and Mem0

        Input: text prompt
        Output: Mem0 data
    """
    multionscrapper = MultiOnUtils()

    retrieve_response = multionscrapper.scrape_github()
    print(retrieve_response)
    print("Step 1 completed")

if __name__ == "__main__":
    main()