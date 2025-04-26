
from web_environment import WebEnvironment
from agent import Agent
from logger import dump_log
import json


tasks_id = [45, 46, 102, 103, 104, 106, 132, 134, 136]

# tasks_id = [102]

env = WebEnvironment()
agent = Agent(is_exploration=True, name="gitlab_fresh_start_3")
for iter_id in range(3):
    for task_id in tasks_id:
        objective, observation = env.load(task_id)
        agent.load(objective, observation)
        final_answer = None
        action_logs = []
        print(f"\n----- TASK ID : {task_id} -----\n")
        # Capping maximum number of steps
        for i in range(100):
            observation, url, screenshot = env.observe()
            name, args, is_page_op, is_final, log_info = agent.get_action(observation, url, screenshot)
            action_logs += [log_info]
            dump_log(action_logs, f"trajectories/{agent.name}/{task_id}/", f"{iter_id}.{task_id}")
            agent.library.save(f"policies/{agent.name}/", f"{iter_id}.{task_id}")
            if is_page_op:
                env.interact(name, args)
            if is_final:
                try:
                    final_answer = args[0]
                except:
                    final_answer = "N/A"
                break    

        print(f"{'-'*10}\nFor the task :\n{objective}\nMy final answer is : {final_answer}\n{'-'*10}\n")


