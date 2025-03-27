import json
import numpy as np
import os
from datetime import datetime
from utils import *

# def get_embedding(text):
#     return np.random.rand(128)  # Example: Returns a random 128-dim vector


class PolicyLibrary:
    def __init__(self, testing=True):
        self.policies = {}
        self.testing = testing

    def update(self, name, description, content=""):
        embedding = get_embedding(description)
        for key, (policy_name, _, _) in self.policies.items():
            if policy_name == name:
                self.policies[key] = (name, description, content)
                return
        self.policies[tuple(embedding)] = (name, description, content)
        if self.testing:
            self.save("policies/testing.json")

    def retrieve(self, description, k=5, exclude_policy=None):
        query_embedding = get_embedding(description)
        
        sorted_policies = sorted(
            self.policies.items(),
            key=lambda item: np.linalg.norm(np.array(item[0]) - query_embedding)
        )
        
        result = []
        for _, (name, desc, _) in sorted_policies:
            if exclude_policy is None or name != exclude_policy:
                result.append((name, desc))
            if len(result) == k:
                break
        
        return result
    
    def get(self, name):
        for _, (policy_name, desc, content) in self.policies.items():
            if policy_name == name:
                return desc, content
        return None

    def save(self, path):
        num_policies = len(self.policies)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        data = {
            "metadata": {
                "num_policies": num_policies,
                "created_at": timestamp
            },
            "policies": [
                {
                    "embedding": ", ".join(map(lambda coord: str(round(coord, 6)), key)),
                    "name": name,
                    "description": desc,
                    "content": content
                }
                for key, (name, desc, content) in self.policies.items()
            ]
        }
        
        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    def load(self, path):
        with open(path, "r") as f:
            data = json.load(f)
        self.policies = {tuple(np.array(list(map(float, item["embedding"].split(", "))))): (item["name"], item["description"], item["content"]) 
                         for item in data["policies"]}
