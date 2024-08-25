from dotenv import load_dotenv
from multion_utils import MultiOnUtils
from mem0_utils import MemorySystem

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

    """
    Step 2 Initialize GraphMemory
    """
    memory_system = MemorySystem()
    memory = memory_system.get_memory()

    """
    Step 2 Memorize
    """
    # repositories = ["mem0ai/mem0", "MULTI-ON/multion-python"]
    # usernames = ["userA", "userB"]
    # # Iterate over the list of repositories
    # for repository in repositories:
    #     print(f"Repository: {repository}")
    #     # Iterate over the list of usernames for each repository
    #     for username in usernames:
    #         print(f"  Username: {username}")
    #         memory.add(f"This repository is starred by this user: {username}", user_id=repository)

    result = memory.add("Likes to play cricket on weekends", user_id="alice", metadata={"category": "hobbies"})


if __name__ == "__main__":
    main()