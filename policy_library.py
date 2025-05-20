import json
import numpy as np
import os
from datetime import datetime
from utils import *

class PolicyLibrary:
    def __init__(self, path=None):
        self.policies = {}
        self.usage_stats = {}  # Track usage and failure counts per policy
        if not (path is None):
            self.load(path)

    def update(self, name, description, content="", site=None):
        embedding = get_embedding(description)
        # for key, (policy_name, _, _) in self.policies.items():
        #     if policy_name == name:
        #         self.policies[key] = (name, description, content, site)
        #         return
        self.policies[tuple(embedding)] = (name, description, content, site)
        self.usage_stats.setdefault(name, {"used": 0, "failed": 0})

    def retrieve(self, description, k=5, exclude_policy=None, site=None):
        query_embedding = get_embedding(description)
        
        sorted_policies = sorted(
            self.policies.items(),
            key=lambda item: np.linalg.norm(np.array(item[0]) - query_embedding)
        )
        
        result = []
        for _, (name, desc, _, s) in sorted_policies:
            if (exclude_policy is None or name != exclude_policy) and (s is None or site is None or s == site):
                result.append((name, desc))
            if len(result) == k:
                break
        
        return result

    def get(self, name):
        for _, (policy_name, desc, content, site) in self.policies.items():
            if policy_name == name:
                return desc, content
        return None

    def is_new(self, name):
        return self.get(name) is None

    def report_use(self, name, is_success):
        if name not in self.usage_stats:
            self.usage_stats[name] = {"used": 0, "failed": 0}
        self.usage_stats[name]["used"] += 1
        if not is_success:
            self.usage_stats[name]["failed"] += 1
        return self.usage_stats[name]["used"], self.usage_stats[name]["failed"]

    def save(self, path=".", name="library"):
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
                    "content": content,
                    "site": site,
                    "used": self.usage_stats.get(name, {}).get("used", 0),
                    "failed": self.usage_stats.get(name, {}).get("failed", 0)
                }
                for key, (name, desc, content, site) in self.policies.items()
            ]
        }
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(f"{path}{name}.json", "w") as f:
            json.dump(data, f, indent="\t")

    def load(self, path):
        with open(path, "r") as f:
            data = json.load(f)
        self.policies = {
            tuple(np.array(list(map(float, item["embedding"].split(", "))))): 
            (item["name"], item["description"], item["content"]) 
            for item in data["policies"]
        }
        self.usage_stats = {
            item["name"]: {"used": item.get("used", 0), "failed": item.get("failed", 0)}
            for item in data["policies"]
        }

        def reset(self, name):
            # Remove usage statistics
            if name in self.usage_stats:
                del self.usage_stats[name]
            # Remove policy entry
            keys_to_delete = [key for key, (policy_name, _, _) in self.policies.items() if policy_name == name]
            for key in keys_to_delete:
                del self.policies[key]


