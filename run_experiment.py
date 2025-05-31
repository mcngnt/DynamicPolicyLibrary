import os
import json
from collections import defaultdict
from utils import *

parent_folder = "trajectories/step_agent_llama"
output_folder = "experiments"
output_file = os.path.join(output_folder, "step.json")

# Dictionary to store scores per site
site_scores = defaultdict(list)

for subfolder in os.listdir(parent_folder):
    subfolder_path = os.path.join(parent_folder, subfolder)
    if not os.path.isdir(subfolder_path):
        continue

    try:
        task_id = int(subfolder)
    except ValueError:
        continue  # skip folders that aren't task IDs

    site = get_site_type(task_id)
    if site == "map":
        continue

    json_file = os.path.join(subfolder_path, f"0.{subfolder}.json")
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            data = json.load(f)
            score = data.get("score")
            if score is not None:
                site_scores[site].append(score)

# Compute average scores per site
result = {}
all_scores = []

for site, scores in site_scores.items():
    all_scores.extend(scores)
    result[site] = {
        "average_score": sum(scores) / len(scores),
        "num_trajectories": len(scores)
    }

# Add overall score
if all_scores:
    result["overall"] = {
        "average_score": sum(all_scores) / len(all_scores),
        "num_trajectories": len(all_scores)
    }

# Create output directory if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Save to step.json
with open(output_file, "w") as f:
    json.dump(result, f, indent=4)