from utils import *
from web_environment import WebEnvironment, AvailableURL
from policy_library import PolicyLibrary

from writing_policy import write_policy
from get_action import get_action
from critique import get_critique
from get_policy import get_policy



tasks = [
("Tell me the full address of all international airports that are within a driving distance of 30 km to Carnegie Art Museum",
AvailableURL.MAP.value, 9, "Pittsburgh International Airport, Southern Beltway, Findlay Township, Allegheny County, 15231, United States"),
("How many commits did kilian make to a11yproject on 3/1/2023?",
AvailableURL.GITLAB.value, 134, "0"),
("List out reviewers, if exist, who mention about ear cups being small", 
AvailableURL.SHOPPING.value + "6s-wireless-headphones-over-ear-noise-canceling-hi-fi-bass-foldable-stereo-wireless-kid-headsets-earbuds-with-built-in-mic-micro-sd-tf-fm-for-iphone-samsung-ipad-pc-black-gold.html", 
21, "unknown"),
("I have a lot of Nintendo Switch game cards now, help me find the best storage option to fit all 31 cards",
AvailableURL.SHOPPING.value, 159, "Unknown")
]

env = WebEnvironment()
policy_library = PolicyLibrary()
for (objective, url, _, _) in [tasks[1]]:
    env.load(url)
    trajectory = [] 
    policy_stack = [{"name":"root", "query":objective, "actions":[]}]
    final_answer = None
    # Capping maximum number of prompt iteration
    for i in range(100):
        observation = env.observe()
        action = {}
        print(f"Here are the current actions performed in the {print_action_call(policy_stack[-1]["name"], [policy_stack[-1]["query"]])} subroutine : {policy_stack[-1]["actions"]}\n")
        if policy_stack[-1]["name"] == "root":
            relevant_policies = policy_library.retrieve(objective)
            policy_feedback = get_policy(objective, observation, "", policy_stack[-1]["actions"], relevant_policies)
            print(f"get_policy feedback : {policy_feedback}\n")
            if policy_feedback["name"].lower() != "stop" and policy_library.is_new(policy_feedback["name"]):
                policy_writing_feedback = write_policy(policy_feedback["name"], policy_feedback["description"], policy_feedback["query"], observation, "", "")
                print(f"write_policy feedback : {policy_writing_feedback}\n")
                policy_library.update(policy_feedback["name"], policy_feedback["description"], policy_writing_feedback["guidance"])
            action = {"name":policy_feedback["name"], "arguments":[policy_feedback["query"]] ,"description":policy_feedback["description"], "is_atomic":0}
        else:
            current_policy_name, current_query, current_actions = policy_stack[-1].values()
            guidance_text = policy_library.get(current_policy_name)[-1]
            policy_objective = print_action_call(current_policy_name, [current_query])
            relevant_policies = policy_library.retrieve(policy_objective, exclude_policy=current_policy_name)
            action = get_action(policy_objective, observation, "", current_actions, guidance_text, relevant_policies)

        policy_stack[-1]["actions"] += [print_action_call(action["name"], action["arguments"])]
        trajectory += [(print_action_call(action["name"], action["arguments"]), observation)]

        if action["name"].lower() == "stop":
            if len(policy_stack) == 1:
                # We just stopped on the root policy
                final_answer = action["arguments"][0]
                break
            prev_policy_name, prev_query, prev_actions = policy_stack.pop().values()
            policy_stack[-1]["actions"] += [print_action_call("stop", action["arguments"])]
            critique_feedback = get_critique(print_action_call(prev_policy_name, [prev_query]), observation, "", prev_actions)
            print(f"get_critique feedback : {critique_feedback}\n")
            if not int(critique_feedback["perfect"]):
                prev_policy_descr, prev_policy_content = policy_library.get(prev_policy_name)
                policy_writing_feedback = write_policy(prev_policy_name, prev_policy_descr, prev_query, prev_actions, critique_feedback["critique"], prev_policy_content)
                print(f"write_policy feedback : {policy_writing_feedback}\n")
                policy_library.update(prev_policy_name, prev_policy_descr, policy_writing_feedback["guidance"])
            continue
        if action["is_atomic"]:
            env.interact(action["name"], action["arguments"])
            continue
        # A this point, the action is not "stop" nor any other atomic action. It is then a policy call
        policy_stack += [{"name":action["name"], "query":action["arguments"][0], "actions":[]}]


    print(f"{'-'*10}\nFor the task :\n{objective}\nMy final answer is : {final_answer}\n{'-'*10}\n")


