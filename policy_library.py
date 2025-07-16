import json
import numpy as np
import os
from datetime import datetime
from utils import *

class PolicyLibrary:
    def __init__(self, path=None, default_path=None):
        self.policies = {}
        self.usage_stats = {}
        if path is not None and os.path.exists(path):
            self.load(path)
        else:
            if default_path is not None and os.path.exists(default_path):
                self.load(default_path)
            else:
                return

    def update(self, name, description, content="", site=None):
        if self.is_new(name):
            embedding = get_embedding(description)
            self.policies[tuple(embedding)] = (name, description, content, site)
            self.usage_stats[name] = {"used": 0, "failed": 0}
        else:
            for e,(policy_name, desc, cont, s) in self.policies.items():
                if policy_name == name:
                    self.policies[e] = (name, desc if len(description)==0 else description, cont if len(content)==0 else content, s if site is None else site)
                    return

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
        print(f"Loaded policy library from {path}.")
        self.policies = {
            tuple(np.array(list(map(float, item["embedding"].split(", "))))): 
            (item["name"], item["description"], item["content"], item["site"]) 
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


