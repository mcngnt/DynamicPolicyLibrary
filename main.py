
from web_environment import WebEnvironment
from agent import Agent
from logger import dump_log
import os
import json

# tasks = [
# ("Tell me the full address of all international airports that are within a driving distance of 30 km to Carnegie Art Museum",
# AvailableURL.MAP.value, 9, "Pittsburgh International Airport, Southern Beltway, Findlay Township, Allegheny County, 15231, United States"),
# ("How many commits did kilian make to a11yproject on 3/1/2023?",
# AvailableURL.GITLAB.value, 134, "0"),
# ("List out reviewers, if exist, who mention about ear cups being small", 
# AvailableURL.SHOPPING.value + "6s-wireless-headphones-over-ear-noise-canceling-hi-fi-bass-foldable-stereo-wireless-kid-headsets-earbuds-with-built-in-mic-micro-sd-tf-fm-for-iphone-samsung-ipad-pc-black-gold.html", 
# 21, "unknown"),
# ("I have a lot of Nintendo Switch game cards now, help me find the best storage option to fit all 31 cards",
# AvailableURL.SHOPPING.value, 159, "Unknown")
# ]

# tasks_id = [45, 46, 102, 103, 104, 106, 132, 134, 136]
tasks_id = [134]


env = WebEnvironment()
agent = Agent(is_exploration=True, name="gitlab_first_exp")
for task_id in tasks_id:
    objective = env.load(task_id)
    agent.load(objective)
    final_answer = None
    action_logs = []
    # Capping maximum number of steps
    for i in range(50):
        observation, url = env.observe()
        name, args, is_page_op, is_final, log_info = agent.get_action(observation, url)
        action_logs += [log_info]
        print(log_info)
        dump_log(action_logs, f"trajectories/{agent.name}_{task_id}")
        if is_page_op:
            env.interact(name, args)
        if is_final:
            final_answer = args[0]
            break    

    print(f"{'-'*10}\nFor the task :\n{objective}\nMy final answer is : {final_answer}\n{'-'*10}\n")


