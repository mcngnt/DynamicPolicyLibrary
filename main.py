
from web_environment import WebEnvironment
from agent import Agent
from step.step_agent import StepAgent
from logger import dump_log
import json
import os

from evaluator import evaluate_task

import numpy as np


import argparse


def main(args):

    print(f"Running with agent_type = {args.agent_type}")

    # tasks_id = [45, 46, 102, 103, 104, 106, 132, 134, 136]

    # tasks_id = np.random.choice(812, size=100, replace=False)

    env = WebEnvironment()


    if args.agent_type == "dynamic":
        agent = Agent(is_exploration=True, name="agent_llama", policy_library_path="policies/agent_llama/0.195.json")
        iter_nb = 3
        save_library = True
        total_nb = 33

    else:
        agent = StepAgent(name="step_agent_llama", policy_library_path="policies/step_policies.json")
        iter_nb = 1
        save_library = False
        total_nb = 100


    mandatory_ids = [int(name) for name in os.listdir(f"trajectories/{agent.name}")]
    remaining_ids = np.setdiff1d(np.arange(812), mandatory_ids)
    random_ids = np.random.choice(remaining_ids, size=total_nb-len(mandatory_ids), replace=False)
    tasks_id = np.concatenate((mandatory_ids, random_ids))


    for iter_id in range(iter_nb):
        for task_id in tasks_id:
            if os.path.exists(f"trajectories/{agent.name}/{task_id}/{iter_id}.{task_id}.json"):
                continue
            print(f"\n----- TASK ID : {task_id} -----\n")
            objective, observation = env.load(task_id)
            agent.load(objective, observation, task_id)
            final_answer = ""
            action_logs = []
            for i in range(45):
                observation, url, screenshot = env.observe()
                name, args, is_page_op, is_final, log_info = agent.get_action(observation, url, screenshot)
                action_logs += [log_info]
                dump_log(action_logs, f"trajectories/{agent.name}/{task_id}/", f"{iter_id}.{task_id}")
                if is_page_op:
                    env.interact(name, args)
                if is_final:
                    try:
                        final_answer = args[0]
                    except:
                        final_answer = "N/A"
                    break    

            print(f"{'-'*10}\nFor the task :\n{objective}\nMy final answer is : {final_answer}\n{'-'*10}\n")
            print(f"Final URL : {env.current_url}")
            score = evaluate_task(task_id, env.webarena_actions_history, env.obs_info_history, env.browserenv_env, final_answer)
            print(f"Final score : {score}")
            dump_log(action_logs, f"trajectories/{agent.name}/{task_id}/", f"{iter_id}.{task_id}", score)
            if save_library:
                agent.library.save(f"policies/{agent.name}/", f"{iter_id}.{task_id}")
                agent.library.save(f"policies/{agent.name}/", f"last")




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--agent_type",
        type=str,
        choices=["dynamic", "step"],
        default="dynamic",
    )
    args = parser.parse_args()
    main(args)
