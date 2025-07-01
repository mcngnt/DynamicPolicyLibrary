import os
import json
from collections import defaultdict
from utils import *

# name = "dynamic_llama_base_step_new_pol"
name = "base"
parent_folder = f"trajectories/{name}"
output_folder = "experiments"
output_file = os.path.join(output_folder, f"{name}.json")

title = "Single LLM"


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
    # if si te == "map":
    #     continue

    json_file = os.path.join(subfolder_path, f"0.{subfolder}.json")
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            data = json.load(f)
            score = data.get("score")
            if score is not None:
                site_scores[site].append(score)


result = {}
all_scores = []

for site, scores in site_scores.items():
    all_scores.extend(scores)
    result[site] = {
        "score": sum(scores) / len(scores),
        "nb": len(scores)
    }

if all_scores:
    result["overall"] = {
        "score": sum(all_scores) / len(all_scores),
        "nb": len(all_scores)
    }

result["title"] = title

os.makedirs(output_folder, exist_ok=True)

with open(output_file, "w") as f:
    json.dump(result, f, indent=4)