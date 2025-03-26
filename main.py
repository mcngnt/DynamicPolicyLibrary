from utils import *
from web_environment import WebEnvironment
from policy_library import PolicyLibrary

from writing_policy import write_policy
from get_action import get_action
from critique import get_critique
from choose_policy import choose_policy

# Functions to quickly test the prompts of the different components :
# from writing_policy import get_my_writing_answer
# from get_action import get_my_action
# from critique import get_my_critique
# from choose_policy import choose_my_policy





tasks = [("Tell me the full address of all international airports that are within a driving distance of 30 km to Carnegie Art Museum", "")]

env = WebEnvironment()
policy_library = PolicyLibrary()
for (objective, url) in tasks:
    env.load(url)
    trajectory = []
    policy_stack = []
    # Capping maximum number of prompt iteration
    for i in range(100):
        observation = env.observe()
        guidance_text = ""
        stack_objective = None
        if len(policy_stack) > 0:
            current_policy_name, current_query, _ = policy_stack[-1]
            guidance_text = policy_library.get(current_policy_name)[-1]
            stack_objective = f"{current_policy_name} [{current_query}]"
        action = get_action(objective if stack_objective is None else stack_objective, observation, url, [print_action_call(a["name"], a["arguments"]) for (a,o) in trajectory], guidance_text)
        print(f"Just got the action : {action}\n")
        trajectory += [(action, observation)]
        if action["name"] == "stop":
            if len(policy_stack) == 0:
                break
            else:
                prev_policy_name, prev_policy_args, prev_policy_iter_start_id = policy_stack.pop()
                critique_feedback = get_critique(objective, observation, url, [print_action_call(a["name"], a["arguments"]) for (a,o) in trajectory])
                print(f"Feedback from the critique after completing the policy {prev_policy_name} : {critique_feedback}\n")
                if not int(critique_feedback["success"]):
                    prev_policy_descr, prev_policy_content = policy_library.get(prev_policy_name)
                    policy_writing_feedback = write_policy(prev_policy_name, prev_policy_descr, prev_policy_args, trajectory[prev_policy_iter_start_id:], critique_feedback["critique"], prev_policy_content)
                    print(f"Just writing guidance for the new policy {action['name']} : {policy_writing_feedback}\n")
                    policy_library.update(prev_policy_name, prev_policy_descr, policy_writing_feedback["guidance"])
            continue
        if action["is_atomic"]:
            env.interact(action["name"], action["arguments"])
            continue
        # A this point, the action is not "stop" nor any other atomic action. It is then a policy call
        relevant_polices = policy_library.retrieve(action["description"])
        choosen_policy_feedback = choose_policy(action["name"], action["arguments"], action["description"], relevant_polices)
        print(f"Trying to choose a policy fitting for the {action['name']} policy call : {choosen_policy_feedback}\n")
        if int(choosen_policy_feedback["new"]):
            policy_writing_feedback = write_policy(action["name"], action["description"], action["arguments"], env.observe(), "", "")
            print(f"Just writing guidance for the new policy {action['name']} : {policy_writing_feedback}\n")
            policy_library.update(action["name"], action["description"], policy_writing_feedback["guidance"])
            policy_stack += [(action["name"], action["arguments"][0], i)]
        else:
            policy_stack += [(choosen_policy_feedback["name"], choosen_policy_feedback["arguments"], i)]



# Testing the components prompts :
# print(get_my_writing_answer())
# print(get_my_action())
# print(get_my_critique())
# print(choose_my_policy())


# Testing policy library :
# policy_library = PolicyLibrary()
# policy_library.load("policies/test_policies.json")
# print(policy_library.retrieve("""CMS""", k=2)
# policy_library.add("find_commits", """Given you are in a project page, this Gitlab subroutine searches for commits made to the project and retrieves information about a commit. This function returns the answer to the query.""")
# policy_library.add("search_issues", """Given you are in my issue page, this Gitlab subroutine searches issues that match the query. Any objective that says "open my latest issue" or "open issue with <keyword> in the title" must be passed through this subroutine.""")
# policy_library.add("find_subreddit", """This Reddit subroutine finds a subreddit corresponding to the query. The query can either be the name of the subreddit or a vague description of what the subreddit may contain. The subroutine hands back control once it navigates to the subreddit.""")
# policy_library.add("find_user", """This Reddit subroutine navigates to the page of a user with user_name. The page contains all the posts made by the user.""")
# policy_library.add("find_order", """This CMS subroutine finds an order corresponding to a particular customer or order number.""")
# policy_library.add("find_customer_review", """This CMS subroutine finds customer reviews for a particular product using the query to specify the kind of review.""")
# policy_library.update("find_subreddit", "FIND SUBREDDIT TEST")
# print(policy_library.get("find_user"))
# print(policy_library.retrieve("""This Reddit subroutine navigates to the page of a user with user_name. The page contains all the posts made by the user.""", k=1))
# print(policy_library.retrieve("""This Reddit subroutine navigates to the page of a user with user_name. The page contains all the posts made by the user.""", k=2))
# print(policy_library.retrieve("""CMS""", k=2))
# policy_library.save("policies/test_policies.json")