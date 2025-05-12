
from web_environment import WebEnvironment
from agent import Agent
from step_agent import StepAgent
from logger import dump_log
import json

from evaluator import evaluate_task

tasks_id = [45, 46, 102, 103, 104, 106, 132, 134, 136]
env = WebEnvironment()



# agent = Agent(is_exploration=True, name="gitlab_fresh_start_3")
# iter_nb = 3
# save_library = True


agent = StepAgent(name="step_agent_1", policy_library_path="policies/step_policies.json")
iter_nb = 1
save_library = False


for iter_id in range(iter_nb):
    for task_id in tasks_id:
        objective, observation = env.load(task_id)
        agent.load(objective, observation, task_id)
        final_answer = ""
        action_logs = []
        print(f"\n----- TASK ID : {task_id} -----\n")
        # Capping maximum number of steps
        for i in range(100):
            observation, url, screenshot = env.observe()
            name, args, is_page_op, is_final, log_info = agent.get_action(observation, url, screenshot)
            action_logs += [log_info]
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