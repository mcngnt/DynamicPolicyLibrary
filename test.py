# Functions to quickly test the prompts of the different components :
# from writing_policy import get_my_writing_answer
# from get_action import get_my_action
# from critique import get_my_critique
# from get_policy import get_my_policy
# from policy_library import PolicyLibrary
# from utils import *
# from web_environment import WebEnvironment, print_gym_call

# from browsergym.core.action.highlevel import HighLevelActionSet
import json

import gymnasium as gym
import browsergym.webarena
from browsergym.utils.obs import flatten_axtree_to_str, flatten_dom_to_str, prune_html

page_op = ["click", "type", "go_back", "go_home", "stop"]

# actions = HighLevelActionSet(
#             subsets=["chat", "tab", "nav", "bid", "infeas"],  # define a subset of the action space
#             # subsets=["chat", "bid", "coord", "infeas"] # allow the agent to also use x,y coordinates
#             strict=False,  # less strict on the parsing of the actions
#             multiaction=False,  # does not enable the agent to take multiple actions at once
#             demo_mode=False,  # add visual effects
#         )

# print(actions.__dict__)

# print(AvailableURL.REDDIT.value)

# print(print_gym_call("go_back", ['42', "Carnegie"]))

# env = WebEnvironment()
# env.load(AvailableURL.REDDIT.value)
# env.interact("type", ["48", "wall", "1"])
# print(env.observe())
# print(env.observe())
# env.interact("go_home", [])
# print(env.observe())

# env.load(AvailableURL.GITLAB.value)

# print(env.observe())

# env.interact("type", ["97", "a11yproject", "1"])

# print(env.observe())

# env.interact("type", [])

# print(get_my_action())
# print(get_my_policy())


# Testing the components prompts :
# print(get_my_writing_answer())
# print(get_my_critique())
# print(choose_my_policy())


# Testing policy library :

# policy_library = PolicyLibrary()

# # policy_library.load("policies/test_policies.json")


# policy_library.update("find_commits", """Given you are in a project page, this Gitlab subroutine searches for commits made to the project and retrieves information about a commit. This function returns the answer to the query.""")
# policy_library.update("search_issues", """Given you are in my issue page, this Gitlab subroutine searches issues that match the query. Any objective that says "open my latest issue" or "open issue with <keyword> in the title" must be passed through this subroutine.""")
# policy_library.update("find_subreddit", """This Reddit subroutine finds a subreddit corresponding to the query. The query can either be the name of the subreddit or a vague description of what the subreddit may contain. The subroutine hands back control once it navigates to the subreddit.""")
# policy_library.update("find_user", """This Reddit subroutine navigates to the page of a user with user_name. The page contains all the posts made by the user.""")
# policy_library.update("find_order", """This CMS subroutine finds an order corresponding to a particular customer or order number.""")
# policy_library.update("find_customer_review", """This CMS subroutine finds customer reviews for a particular product using the query to specify the kind of review.""")



# print(policy_library.retrieve("github", k=5, exclude_policy="find_commits"))



# policy_library.update("find_subreddit", "FIND SUBREDDIT TEST")
# print(policy_library.get("find_user"))
# print(policy_library.retrieve("""This Reddit subroutine navigates to the page of a user with user_name. The page contains all the posts made by the user.""", k=1))
# print(policy_library.retrieve("""This Reddit subroutine navigates to the page of a user with user_name. The page contains all the posts made by the user.""", k=2))
# print(policy_library.retrieve("""CMS""", k=2))
# policy_library.save("policies/test_policies.json")

# print(parse_action_call("function_name"))  # ['function_name']
# print(parse_action_call("function_name[arg1] [arg2][arg3]"))  # ['function_name', 'arg1', 'arg2', 'arg3']
# print(parse_action_call("function_name [arg1]   [arg2][arg3]"))  # ['function_name', 'arg1', 'arg2', 'arg3']











# def nb_policies(id):
#     with open(f"../../step_trajectories/{id}.json", "r") as f:
#         data = json.load(f)


#     actions = [parse_action_call(step["action"])[0] for step in data.get("trajectory", []) if "action" in step]

#     return sum([not (action in page_op) for action in actions])


# multiple_actions_tasks_nb = 0
# tasks_nb = 0

# for i in range(811):
#     try:
#         n = nb_policies(i)
#         tasks_nb += 1
#         if n >= 1:
#             print(f"{i} : {n}")
#             multiple_actions_tasks_nb += 1
#     except:
#         print(f"Error with file {i}")


# print((multiple_actions_tasks_nb / tasks_nb)*100)

# # 53.67% of tasks use at least one policy
# # 23.41% of tasks use more than 1 policy













# # start a webarena task
# env = gym.make("browsergym/webarena.7")

# obs, info = env.reset()


# print(obs.keys())

# print(obs["goal"])
# print(flatten_axtree_to_str(obs["axtree_object"]))
# # list all the available webarena tasks
# env_ids = [id for id in gym.envs.registry.keys() if id.startswith("browsergym/webarena")]
# print("\n".join(env_ids))







from logger import dump_log

# actions = [
#     {"objective":"find X", "observation":"observation", "guidance":"no","relevant_policies":None, "action":None, "is_page_op":None, "is_stop":None, "reason":None, "description":None,"critique":None, "plan":None, "created_policies":None}
#     {"name": "start root logic", "description": "start root logic", "is_page_op": True, "is_stop": False, "commentary": None},
#     {"name": "foo", "description": "Foo does intermediate stuff", "is_page_op": False, "is_stop": False, "commentary": None},
#     {"name": "doing something in foo", "description": "doing something in foo", "is_page_op": True, "is_stop": False, "commentary": None},
#     {"name": "baz", "description": "Baz is low-level", "is_page_op": False, "is_stop": False, "commentary": None},
#     {"name": "inside baz", "description": "inside baz", "is_page_op": True, "is_stop": False, "commentary": None},
#     {"name": "baz", "description": "", "is_page_op": False, "is_stop": True, "commentary": "bye world"},
#     {"name": "foo", "description": "", "is_page_op": False, "is_stop": True, "commentary": "bye world"},
#     {"name": "bar", "description": "Bar does a thing", "is_page_op": False, "is_stop": False, "commentary": None},
#     {"name": "doing something in bar", "description": "doing something in bar", "is_page_op": True, "is_stop": False, "commentary": None},
#     {"name": "bar", "description": "", "is_page_op": False, "is_stop": True, "commentary": "bye world"},
#     {"name": "end root logic", "description": "end root logic", "is_page_op": True, "is_stop": False, "commentary": None},
#     {"name": "root", "description": "", "is_page_op": False, "is_stop": True, "commentary": "bye world"},
# ]



# actions = [
#     {'objective': 'Check out the most recent open issues', 'observation': None, 'guidance': '', 'relevant_policies': [('FilterAndSortIssues', 'Filters and sorts the issues on the issues page based on given criteria.'), ('ClickLink', 'Clicks a link with the specified text.')], 'action': 'click [328]', 'is_page_op': True, 'is_stop': False, 'reason': 'To check out the most recent open issues, I need to navigate to the "Issues" page. Looking at the current page, there are two "Issues" links. One under "Project navigation" [328] and the other on the top right of the page [183]. Since the objective is to check the project\'s issues, I will use the "Issues" link under "Project navigation".', 'description': None, 'critique': None, 'plan': 'Navigate to the issues page. |  Then, filter and sort the issues to display the most recent open ones.', 'created_policies': [{'name': 'ClickLink', 'description': 'Clicks a link with the specified text.', 'query': 'Issues'}, {'name': 'FilterAndSortIssues', 'description': 'Filters and sorts the issues on the issues page based on given criteria.', 'query': 'open; sort by: created date'}]},
#     {'objective': 'Check out the most recent open issues', 'observation': None, 'guidance': '', 'relevant_policies': [('FilterAndSortIssues', 'Filters and sorts the issues on the issues page based on given criteria.'), ('ClickLink', 'Clicks a link with the specified text.')], 'action': 'click [668]', 'is_page_op': True, 'is_stop': False, 'reason': 'The issues are currently sorted by "Created date" in descending order. To find the most recent issues, I need to sort them by "Created date" in ascending order.', 'description': None, 'critique': None, 'plan': None, 'created_policies': None},
#     {'objective': 'Check out the most recent open issues', 'observation': None, 'guidance': '', 'relevant_policies': [('FilterAndSortIssues', 'Filters and sorts the issues on the issues page based on given criteria.'), ('ClickLink', 'Clicks a link with the specified text.')], 'action': 'click [724]', 'is_page_op': True, 'is_stop': False, 'reason': 'The objective is to check the most recent open issues. The issues are currently sorted by "Created date". To find the most recent, I need to change the sorting order to ascending. This can be done by clicking the \'Sort direction: Descending\' button.', 'description': None, 'critique': None, 'plan': None, 'created_policies': None},
#     {'objective': 'Check out the most recent open issues', 'observation': None, 'guidance': '', 'relevant_policies': [('FilterAndSortIssues', 'Filters and sorts the issues on the issues page based on given criteria.'), ('ClickLink', 'Clicks a link with the specified text.')], 'action': 'click [724]', 'is_page_op': True, 'is_stop': False, 'reason': 'The objective is to check out the most recent open issues. The issues are currently sorted by created date, ascending, meaning the oldest issues are shown first. To see the newest issues, I need to sort the issues by created date in descending order.', 'description': None, 'critique': None, 'plan': None, 'created_policies': None},
#     {'objective': 'Check out the most recent open issues', 'observation': None, 'guidance': '', 'relevant_policies': [('FilterAndSortIssues', 'Filters and sorts the issues on the issues page based on given criteria.'), ('ClickLink', 'Clicks a link with the specified text.')], 'action': 'stop [N/A]', 'is_page_op': False, 'is_stop': True, 'reason': 'The page is already displaying the open issues sorted by created date, descending. I can now examine the issues.', 'description': None, 'critique': None, 'plan': None, 'created_policies': None},
# ]




# dump_log(actions)





from openai import OpenAI
# Modify OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiYXRsYXMiLCJzYXR1cm4tYXV0aC1wcm94eSJdLCJpc3MiOiJhdGxhcyIsInN1YiI6IjhkMGVjMzMyODg4NTRlMTQ5NWNiMTg0NDYzM2U3YmExIiwiaXNfcmVmcmVzaCI6ZmFsc2UsInVzZXJfaWQiOiJlNjNkNzExNTU0NGQ0MzY2OGQ3Mjk0NGY0M2U3OTY1YyJ9.KTZqy_7jprNOjQ1xKmBiOHmXJi8PhZNB9_TULJmY3Yo-AeWj5JORuZMAOSWb7RbLw6TcxPNsOtZDjNJ0wAKvPRFjMiuuh3OekGrjR0jsdSpHyAguWUEyISq6oSDgNUN-Kb5A_nUUNeZsUyatkQDurxmTAVQ7CVQqxrcJ6tXViDKytAgZj-YtkKW3XQ77fcfMOObw8NuOLeodivQQXXkW1VJIvap5f2ogyO15ZYijEdixAoBxBK5_YAeb8OyutD6rpDR0983siNhHoj_r65c0RlVnhC-li6t4sxp-LNcLk-iVBrH0eNAlU9O2-PTgeJk4JPGiDXhFzS_MjoeeIbdJQY4nCZ0x3CZN6WNaKp-jKN-IKxVCej5Wk-nkLTLZEwRST16icKohVRjCLP4SHczwI64ksoRrhTN2apXeAPlrrhm3uUHFKCUN842AhSpVYY3EDIvHArXd4sQHoph0X76D7bXPnZKVmYPS3FL88NRdYOKqNmeaQBTXqtJ9Vzy8Q2MWBk90RoU83e0zNdKPLJOpuApOcfQ01OXYiPjqfKAMFJcM70bnLdnm5SAtdzZDnRLZ8aU-S2qomVoEFGBYvZ7XuiLtZKHmr1k4HWyFApD2EUKsFqI2Cgm_lf_moMCS0DWgOWrX4N3Lo56Djm0LVEDbyieMvluxOB9YmfaAMVBN7Q8"
openai_api_base = "https://pd-jerom-llama-31-8f1c2f4f76304a54aa1e7b98c596ee59.nvidia-oci.saturnenterprise.io/v1"
client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)
chat_response = client.chat.completions.create(
    model="meta-llama/Llama-3.1-70B-Instruct",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Tell me a joke."},
    ]
)
print("Chat response:", chat_response)