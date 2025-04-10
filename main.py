
from web_environment import WebEnvironment
from agent import Agent
from logger import dump_log
import json


tasks_id = [45, 46, 102, 103, 104, 106, 132, 134, 136]

env = WebEnvironment()
agent = Agent(is_exploration=True, name="gitlab_2nd_exp", policy_library_path="policies/gitlab_2nd_exp.json")
for task_id in tasks_id:
    objective = env.load(task_id)
    agent.load(objective)
    final_answer = None
    action_logs = []
    # Capping maximum number of steps
    for i in range(100):
        observation, url = env.observe()
        name, args, is_page_op, is_final, log_info = agent.get_action(observation, url)
        action_logs += [log_info]
        dump_log(action_logs, f"trajectories/{agent.name}/{task_id}")
        if is_page_op:
            env.interact(name, args)
        if is_final:
            try:
                final_answer = args[0]
            except:
                final_answer = "N/A"
            break    

    print(f"{'-'*10}\nFor the task :\n{objective}\nMy final answer is : {final_answer}\n{'-'*10}\n")


