import os
import json

def is_map(task_id):
    config_file = f"custom_webarena/config_files/{task_id}.json"
    with open(config_file, 'r') as file:
        data = json.load(file)

    return "map" in data.get('sites', [])

parent_folder = "trajectories/step_agent_llama"

scores = []


for subfolder in os.listdir(parent_folder):
    subfolder_path = os.path.join(parent_folder, subfolder)
    task_id = int(subfolder)
    if is_map(task_id):
        continue
    if os.path.isdir(subfolder_path):
        json_file = os.path.join(subfolder_path, f"0.{subfolder}.json")
        with open(json_file, 'r') as f:
            data = json.load(f)
            score = data.get("score")
            if score is not None:
                scores.append(score)



print(len(scores))

if scores:
    average = sum(scores) / len(scores)
    print("Average score:", average)