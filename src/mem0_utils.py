# https://docs.mem0.ai/platform/quickstart

import os
from mem0 import MemoryClient
from mem0 import Memory


class MemorySystem:
    def __init__(self):
        # Get your API key from https://app.mem0.ai/dashboard/api-keys
        self.mem0_api_key = os.environ.get("MEM0_API_KEY")
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")

        self.neo4j_uri = os.environ.get("NEO4J_URI")
        self.neo4j_username = os.environ.get("NEO4J_USERNAME")
        self.neo4j_password = os.environ.get("NEO4J_PASSWORD")

        client = MemoryClient(api_key=self.mem0_api_key)
        self.config = {
            f"graph_store": {
                "provider": "neo4j",
                "config": {
                    "url": f"{self.neo4j_uri}",
                    "username": f"{self.neo4j_username}",
                    "password": f"{self.neo4j_password}"
                }
            },
            "version": "v1.1"
        }

    def get_memory(self):
        m = Memory.from_config(config_dict=self.config)
        return m