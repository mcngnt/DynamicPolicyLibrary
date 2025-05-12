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

from prompts.critique import get_critique
from prompts.writing_policy import write_policy

from utils import *

from logger import dump_log

page_op = ["click", "type", "go_back", "go_home", "stop"]


# help(browsergym.webarena)

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





# from openai import OpenAI
# # Modify OpenAI's API key and API base to use vLLM's API server.
# openai_api_key = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiYXRsYXMiLCJzYXR1cm4tYXV0aC1wcm94eSJdLCJpc3MiOiJhdGxhcyIsInN1YiI6IjhkMGVjMzMyODg4NTRlMTQ5NWNiMTg0NDYzM2U3YmExIiwiaXNfcmVmcmVzaCI6ZmFsc2UsInVzZXJfaWQiOiJlNjNkNzExNTU0NGQ0MzY2OGQ3Mjk0NGY0M2U3OTY1YyJ9.KTZqy_7jprNOjQ1xKmBiOHmXJi8PhZNB9_TULJmY3Yo-AeWj5JORuZMAOSWb7RbLw6TcxPNsOtZDjNJ0wAKvPRFjMiuuh3OekGrjR0jsdSpHyAguWUEyISq6oSDgNUN-Kb5A_nUUNeZsUyatkQDurxmTAVQ7CVQqxrcJ6tXViDKytAgZj-YtkKW3XQ77fcfMOObw8NuOLeodivQQXXkW1VJIvap5f2ogyO15ZYijEdixAoBxBK5_YAeb8OyutD6rpDR0983siNhHoj_r65c0RlVnhC-li6t4sxp-LNcLk-iVBrH0eNAlU9O2-PTgeJk4JPGiDXhFzS_MjoeeIbdJQY4nCZ0x3CZN6WNaKp-jKN-IKxVCej5Wk-nkLTLZEwRST16icKohVRjCLP4SHczwI64ksoRrhTN2apXeAPlrrhm3uUHFKCUN842AhSpVYY3EDIvHArXd4sQHoph0X76D7bXPnZKVmYPS3FL88NRdYOKqNmeaQBTXqtJ9Vzy8Q2MWBk90RoU83e0zNdKPLJOpuApOcfQ01OXYiPjqfKAMFJcM70bnLdnm5SAtdzZDnRLZ8aU-S2qomVoEFGBYvZ7XuiLtZKHmr1k4HWyFApD2EUKsFqI2Cgm_lf_moMCS0DWgOWrX4N3Lo56Djm0LVEDbyieMvluxOB9YmfaAMVBN7Q8"
# openai_api_base = "https://pd-jerom-llama-33-16406b4644034adb887f0a7595866014.nvidia-oci.saturnenterprise.io/v1 "
# client = OpenAI(
#     api_key=openai_api_key,
#     base_url=openai_api_base,
# )
# chat_response = client.chat.completions.create(
#     model="meta-llama/Llama-3.3-70B-Instruct",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "Tell me a joke."},
#     ]
# )
# print("Chat response:", chat_response)


def extract_actions_and_reasons(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    actions_and_reasons = []
    
    for item in data.get("trace", []):
        action = item.get("action")
        reason = item.get("reason")
        if action and reason:
            actions_and_reasons.append((action, reason))
    
    return actions_and_reasons


file_path = "test.json"  # Replace with your actual file path
# previous_actions = extract_actions_and_reasons(file_path)


obs = """
RootWebArea 'Issues \u00b7 Byte Blaze / a11y-webring.club \u00b7 GitLab', focused, url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/issues/?sort=title_asc&state=opened&label_name%5B%5D=help%20wanted&first_page_size=20'\n\t[65] banner ''\n\t\t[66] link 'Skip to content', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/issues/?sort=title_asc&state=opened&label_name%5B%5D=help%20wanted&first_page_size=20#content-body'\n\t\tStaticText 'GitLab'\n\t\t[72] link 'Dashboard', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/'\n\t\t\t[73] image ''\n\t\t[76] list ''\n\t\t\t[77] listitem ''\n\t\t\t\t[78] button '', hasPopup='menu', expanded=False\n\t\t[138] list ''\n\t\t\t[139] listitem ''\n\t\t\t\t[143] image ''\n\t\t\t\t[144] textbox 'Search GitLab'\n\t\t\t\tStaticText '/'\n\t\t[156] list ''\n\t\t\t[157] listitem ''\n\t\t\t\t[158] link 'Create new...', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/projects/new'\n\t\t\t\t\t[159] image ''\n\t\t\t\t\t[160] image ''\n\t\t\t[180] listitem ''\n\t\t\t\t[181] link 'Issues', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/dashboard/issues?assignee_username=byteblaze'\n\t\t\t\t\t[182] image ''\n\t\t\t[184] listitem ''\n\t\t\t\t[185] link 'Merge requests', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/dashboard/merge_requests?assignee_username=byteblaze'\n\t\t\t\t\t[186] image ''\n\t\t\t\t\t[188] image ''\n\t\t\t[198] listitem ''\n\t\t\t\t[199] link 'To-Do List', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/dashboard/todos'\n\t\t\t\t\t[200] image ''\n\t\t\t\t\tStaticText '5'\n\t\t\t[202] listitem ''\n\t\t\t\t[203] link 'Help', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/help'\n\t\t\t\t\tStaticText 'Help'\n\t\t\t\t\t[205] image ''\n\t\t\t\t\t[207] image ''\n\t\t\t[228] listitem ''\n\t\t\t\t[229] link 'Byte Blaze', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze'\n\t\t\t\t\t[230] image 'Byte Blaze', url='https://www.gravatar.com/avatar/99a4297c867eada2606b9b6973f081f9?s=48&d=identicon'\n\t\t\t\t\t[231] image ''\n\t[267] complementary 'Project navigation'\n\t\t[269] list ''\n\t\t\t[270] listitem 'a11y-webring.club'\n\t\t\t\t[271] link 'a11y-webring.club', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club'\n\t\t\t\t\tStaticText 'A'\n\t\t\t\t\tStaticText 'a11y-webring.club'\n\t\t\t[275] listitem ''\n\t\t\t\t[276] link 'Project information', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/activity'\n\t\t\t\t\t[278] image ''\n\t\t\t\t\tStaticText 'Project information'\n\t\t\t[294] listitem ''\n\t\t\t\t[295] link 'Repository', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/tree/main'\n\t\t\t\t\t[297] image ''\n\t\t\t\t\tStaticText 'Repository'\n\t\t\t[325] listitem ''\n\t\t\t\t[326] link 'Issues', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/issues'\n\t\t\t\t\t[328] image ''\n\t\t\t\t\tStaticText 'Issues'\n\t\t\t\t\tStaticText '4'\n\t\t\t\t[331] list ''\n\t\t\t\t\t[337] listitem ''\n\t\t\t\t\t\t[338] link 'Issues', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/issues'\n\t\t\t\t\t\t\tStaticText 'List'\n\t\t\t\t\t[340] listitem ''\n\t\t\t\t\t\t[341] link 'Boards', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/boards'\n\t\t\t\t\t\t\tStaticText 'Boards'\n\t\t\t\t\t[343] listitem ''\n\t\t\t\t\t\t[344] link 'Service Desk', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/issues/service_desk'\n\t\t\t\t\t\t\tStaticText 'Service Desk'\n\t\t\t\t\t[346] listitem ''\n\t\t\t\t\t\t[347] link 'Milestones', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/milestones'\n\t\t\t\t\t\t\tStaticText 'Milestones'\n\t\t\t[349] listitem ''\n\t\t\t\t[350] link 'Merge requests', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/merge_requests'\n\t\t\t\t\t[352] image ''\n\t\t\t\t\tStaticText 'Merge requests'\n\t\t\t\t\tStaticText '1'\n\t\t\t[360] listitem ''\n\t\t\t\t[361] link 'CI/CD', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/pipelines'\n\t\t\t\t\t[363] image ''\n\t\t\t\t\tStaticText 'CI/CD'\n\t\t\t[382] listitem ''\n\t\t\t\t[383] link 'Security & Compliance', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/security/configuration'\n\t\t\t\t\t[385] image ''\n\t\t\t\t\tStaticText 'Security & Compliance'\n\t\t\t[395] listitem ''\n\t\t\t\t[396] link 'Deployments', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/environments'\n\t\t\t\t\t[398] image ''\n\t\t\t\t\tStaticText 'Deployments'\n\t\t\t[414] listitem ''\n\t\t\t\t[415] link 'Packages and registries', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/packages'\n\t\t\t\t\t[417] image ''\n\t\t\t\t\tStaticText 'Packages and registries'\n\t\t\t[430] listitem ''\n\t\t\t\t[431] link 'Infrastructure', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/clusters'\n\t\t\t\t\t[433] image ''\n\t\t\t\t\tStaticText 'Infrastructure'\n\t\t\t[449] listitem ''\n\t\t\t\t[450] link 'Monitor', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/metrics'\n\t\t\t\t\t[452] image ''\n\t\t\t\t\tStaticText 'Monitor'\n\t\t\t[471] listitem ''\n\t\t\t\t[472] link 'Analytics', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/value_stream_analytics'\n\t\t\t\t\t[474] image ''\n\t\t\t\t\tStaticText 'Analytics'\n\t\t\t[490] listitem ''\n\t\t\t\t[491] link 'Wiki', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/wikis/home'\n\t\t\t\t\t[493] image ''\n\t\t\t\t\tStaticText 'Wiki'\n\t\t\t[499] listitem ''\n\t\t\t\t[500] link 'Snippets', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/snippets'\n\t\t\t\t\t[502] image ''\n\t\t\t\t\tStaticText 'Snippets'\n\t\t\t[508] listitem ''\n\t\t\t\t[509] link 'Settings', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/edit'\n\t\t\t\t\t[511] image ''\n\t\t\t\t\tStaticText 'Settings'\n\t\t[560] button 'Collapse sidebar'\n\t\t\t[561] image ''\n\t\t\tStaticText 'Collapse sidebar'\n\t[569] navigation 'Breadcrumbs'\n\t\t[575] list ''\n\t\t\t[576] listitem ''\n\t\t\t\t[577] link 'Byte Blaze', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze'\n\t\t\t\t[578] image ''\n\t\t\t[579] listitem ''\n\t\t\t\t[580] link 'a11y-webring.club', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club'\n\t\t\t\t\tStaticText 'a11y-webring.club'\n\t\t\t\t[582] image ''\n\t\t\t[583] listitem ''\n\t\t\t\t[584] link 'Issues', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/issues'\n\t[587] main ''\n\t\t[595] tablist '', multiselectable=False, orientation='horizontal'\n\t\t\t[597] tab 'Open 2', selected=True, controls='__BVID__9'\n\t\t\t\tStaticText 'Open'\n\t\t\t\tStaticText '2'\n\t\t\t[601] tab 'Closed 0', selected=False\n\t\t\t\tStaticText 'Closed'\n\t\t\t\tStaticText '0'\n\t\t\t[605] tab 'All 2', selected=False\n\t\t\t\tStaticText 'All'\n\t\t\t\tStaticText '2'\n\t\t[609] tabpanel 'Open 2'\n\t\t[613] link 'Subscribe to RSS feed', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/issues.atom?feed_token=TMN_bBn9Z48qVbUFZV45&label_name%5B%5D=help+wanted'\n\t\t[615] link 'Subscribe to calendar', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/issues.ics?due_date=next_month_and_previous_two_weeks&feed_token=TMN_bBn9Z48qVbUFZV45&label_name%5B%5D=help+wanted&sort=closest_future_date'\n\t\t[618] group ''\n\t\t\t[619] button 'Export as CSV'\n\t\t\t[622] button 'Import issues', hasPopup='menu', expanded=False\n\t\t\t\tStaticText 'Import issues'\n\t\t[637] button 'Edit issues'\n\t\t\tStaticText 'Edit issues'\n\t\t[639] link 'New issue', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/issues/new'\n\t\t\tStaticText 'New issue'\n\t\t[642] group ''\n\t\t\t[645] button 'Toggle history', hasPopup='menu', expanded=False\n\t\t\t\tStaticText 'Toggle history'\n\t\t\tStaticText 'Label'\n\t\t\tStaticText '='\n\t\t\tStaticText '~help wanted'\n\t\t\t[1069] button 'Close'\n\t\t\t[675] button 'Clear'\n\t\t\t[678] button 'Search'\n\t\t[680] group ''\n\t\t\t[682] button 'Title', hasPopup='menu', expanded=False\n\t\t\t\tStaticText 'Title'\n\t\t\t[738] button 'Sort direction: Ascending', focused, describedby='__bv_tooltip_106__'\n\t\t[740] complementary '', live='polite', relevant='additions text'\n\t\t[742] list ''\n\t\t\t[1074] listitem ''\n\t\t\t\t[1077] link '[Feature suggestion] Color theme slider', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/issues/21'\n\t\t\t\tStaticText '1 of 3 checklist items completed'\n\t\t\t\tStaticText 'Issue'\n\t\t\t\tStaticText '#21'\n\t\t\t\tStaticText ''\n\t\t\t\tStaticText 'created'\n\t\t\t\tStaticText '2 years ago'\n\t\t\t\tStaticText 'by'\n\t\t\t\t[1088] link 'Byte Blaze', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze'\n\t\t\t\t\tStaticText 'Byte Blaze'\n\t\t\t\tStaticText ''\n\t\t\t\t[1091] group 'Labels'\n\t\t\t\t\t[1093] link 'feature', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/issues/?label_name[]=feature'\n\t\t\t\t\t\tStaticText 'feature'\n\t\t\t\t\t[1096] link 'help wanted', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/issues/?label_name[]=help%20wanted'\n\t\t\t\t\t\tStaticText 'help wanted'\n\t\t\t\t[1099] list ''\n\t\t\t\t\t[1100] listitem ''\n\t\t\t\t\t[1101] listitem ''\n\t\t\t\t\t\t[1103] link 'Assigned to Byte Blaze', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze'\n\t\t\t\t\t\t\t[1105] image 'Assigned to Byte Blaze', url='https://www.gravatar.com/avatar/99a4297c867eada2606b9b6973f081f9?s=80&d=identicon'\n\t\t\t\t\t[1106] list ''\n\t\t\t\t\t[1107] listitem ''\n\t\t\t\t\t\t[1108] link '0', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/issues/21#notes'\n\t\t\t\tStaticText 'updated 2 years ago'\n\t\t\t[1111] listitem ''\n\t\t\t\t[1114] link '[Feature suggestion] WCAG trash panda mode', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/issues/39'\n\t\t\t\tStaticText '1 of 3 checklist items completed'\n\t\t\t\tStaticText 'Issue'\n\t\t\t\tStaticText '#39'\n\t\t\t\tStaticText ''\n\t\t\t\tStaticText 'created'\n\t\t\t\tStaticText '2 years ago'\n\t\t\t\tStaticText 'by'\n\t\t\t\t[1125] link 'Byte Blaze', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze'\n\t\t\t\t\tStaticText 'Byte Blaze'\n\t\t\t\tStaticText ''\n\t\t\t\t[1128] group 'Labels'\n\t\t\t\t\t[1130] link 'feature', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/issues/?label_name[]=feature'\n\t\t\t\t\t\tStaticText 'feature'\n\t\t\t\t\t[1133] link 'help wanted', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/issues/?label_name[]=help%20wanted'\n\t\t\t\t\t\tStaticText 'help wanted'\n\t\t\t\t[1136] list ''\n\t\t\t\t\t[1137] listitem ''\n\t\t\t\t\t[1138] listitem ''\n\t\t\t\t\t\t[1140] link 'Assigned to Byte Blaze', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze'\n\t\t\t\t\t\t\t[1142] image 'Assigned to Byte Blaze', url='https://www.gravatar.com/avatar/99a4297c867eada2606b9b6973f081f9?s=80&d=identicon'\n\t\t\t\t\t[1143] list ''\n\t\t\t\t\t[1144] listitem ''\n\t\t\t\t\t\t[1145] link '0', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/issues/39#notes'\n\t\t\t\tStaticText 'updated 2 years ago'\n\t\t[818] complementary 'Bulk update', live='polite', relevant='additions text'\n\t[1148] tooltip 'Sort direction: Ascending'\n\t\tStaticText 'Sort direction: Ascending'
"""

init_obs = """
RootWebArea 'Issues \u00b7 Dashboard \u00b7 GitLab', focused, url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/dashboard/issues?assignee_username=byteblaze'\n\t[63] banner ''\n\t\t[64] link 'Skip to content', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/dashboard/issues?assignee_username=byteblaze#content-body'\n\t\tStaticText 'GitLab'\n\t\t[70] link 'Dashboard', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/'\n\t\t\t[71] image ''\n\t\t[74] list ''\n\t\t\t[75] listitem ''\n\t\t\t\t[76] button '', hasPopup='menu', expanded=False\n\t\t[117] list ''\n\t\t\t[118] listitem ''\n\t\t\t\t[122] image ''\n\t\t\t\t[123] textbox 'Search GitLab'\n\t\t\t\tStaticText '/'\n\t\t[132] list ''\n\t\t\t[133] listitem ''\n\t\t\t\t[134] link 'Create new...', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/projects/new'\n\t\t\t\t\t[135] image ''\n\t\t\t\t\t[136] image ''\n\t\t\t[145] listitem ''\n\t\t\t\t[146] link 'Issues', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/dashboard/issues?assignee_username=byteblaze'\n\t\t\t\t\t[147] image ''\n\t\t\t[149] listitem ''\n\t\t\t\t[150] link 'Merge requests', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/dashboard/merge_requests?assignee_username=byteblaze'\n\t\t\t\t\t[151] image ''\n\t\t\t\t\t[153] image ''\n\t\t\t[163] listitem ''\n\t\t\t\t[164] link 'To-Do List', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/dashboard/todos'\n\t\t\t\t\t[165] image ''\n\t\t\t\t\tStaticText '5'\n\t\t\t[167] listitem ''\n\t\t\t\t[168] link 'Help', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/help'\n\t\t\t\t\tStaticText 'Help'\n\t\t\t\t\t[170] image ''\n\t\t\t\t\t[172] image ''\n\t\t\t[193] listitem ''\n\t\t\t\t[194] link 'Byte Blaze', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze'\n\t\t\t\t\t[195] image 'Byte Blaze', url='https://www.gravatar.com/avatar/99a4297c867eada2606b9b6973f081f9?s=48&d=identicon'\n\t\t\t\t\t[196] image ''\n\t[236] main ''\n\t\t[239] heading 'Issues'\n\t\t[242] link 'Select project to create issue', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/dashboard/issues?assignee_username=byteblaze'\n\t\t[257] button 'Toggle project select'\n\t\t[259] list ''\n\t\t\t[260] listitem ''\n\t\t\t\t[261] link 'Open 13', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/dashboard/issues?assignee_username=byteblaze&state=opened'\n\t\t\t\t\tStaticText 'Open'\n\t\t\t\t\tStaticText '13'\n\t\t\t[264] listitem ''\n\t\t\t\t[265] link 'Closed 53', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/dashboard/issues?assignee_username=byteblaze&state=closed'\n\t\t\t\t\tStaticText 'Closed'\n\t\t\t\t\tStaticText '53'\n\t\t\t[268] listitem ''\n\t\t\t\t[269] link 'All 66', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/dashboard/issues?assignee_username=byteblaze&state=all'\n\t\t\t\t\tStaticText 'All'\n\t\t\t\t\tStaticText '66'\n\t\t[273] link 'Subscribe to RSS feed', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/dashboard/issues.atom?assignee_username=byteblaze&feed_token=TMN_bBn9Z48qVbUFZV45&state=opened'\n\t\t\t[274] image ''\n\t\t\tStaticText 'Subscribe to RSS feed'\n\t\t[276] link 'Subscribe to calendar', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/dashboard/issues.ics?assignee_username=byteblaze&due_date=next_month_and_previous_two_weeks&feed_token=TMN_bBn9Z48qVbUFZV45&sort=closest_future_date&state=opened'\n\t\t\t[277] image ''\n\t\t\tStaticText 'Subscribe to calendar'\n\t\t[286] button 'Recent searches'\n\t\t\tStaticText 'Recent searches'\n\t\t\t[291] image ''\n\t\t[312] list ''\n\t\t\t[313] listitem ''\n\t\t\t\t[314] button 'Assignee = Byte Blaze'\n\t\t\t\t\tStaticText 'Assignee'\n\t\t\t\t\tStaticText '='\n\t\t\t\t\t[319] image '', url='https://www.gravatar.com/avatar/99a4297c867eada2606b9b6973f081f9?s=80&d=identicon'\n\t\t\t\t\tStaticText 'Byte Blaze'\n\t\t\t\t\t[320] button ''\n\t\t\t\t\t\t[321] image ''\n\t\t\t[322] listitem ''\n\t\t\t\t[323] textbox ''\n\t\t[509] button ''\n\t\t\t[510] image ''\n\t\t[513] group ''\n\t\t\t[515] button 'Priority', hasPopup='listbox'\n\t\t\t\tStaticText 'Priority'\n\t\t\t[562] link 'Sort direction', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/dashboard/issues?assignee_username=byteblaze&sort=created_asc'\n\t\t\t\t[563] image ''\n\t\t[564] list ''\n\t\t\t[565] listitem ''\n\t\t\t\t[570] link '[Feature suggestion] Support linking to an accessibility statement', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/issues/71'\n\t\t\t\tStaticText '1 of 3 checklist items completed'\n\t\t\t\tStaticText 'byteblaze/a11y-webring.club#71'\n\t\t\t\tStaticText '\u00b7 created'\n\t\t\t\t[575] time 'Feb 2, 2023 9:51pm UTC'\n\t\t\t\t\tStaticText '2 years ago'\n\t\t\t\tStaticText 'by'\n\t\t\t\t[576] link 'Rohan Kumar', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/Seirdy'\n\t\t\t\t\tStaticText 'Rohan Kumar'\n\t\t\t\tStaticText ''\n\t\t\t\t[579] link 'being discussed', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/issues?label_name%5B%5D=being+discussed'\n\t\t\t\t\tStaticText 'being discussed'\n\t\t\t\t[582] link 'feature', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/issues?label_name%5B%5D=feature'\n\t\t\t\t\tStaticText 'feature'\n\t\t\t\t[585] list ''\n\t\t\t\t\t[586] listitem ''\n\t\t\t\t\t\t[587] link 'Assigned to Byte Blaze', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze'\n\t\t\t\t\t\t\t[588] image '', url='https://www.gravatar.com/avatar/99a4297c867eada2606b9b6973f081f9?s=32&d=identicon'\n\t\t\t\t\t[589] listitem ''\n\t\t\t\t\t\t[590] link '1', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/issues/71#notes'\n\t\t\t\t\t\t\t[591] image ''\n\t\t\t\tStaticText 'updated'\n\t\t\t\t[594] time 'Mar 27, 2023 9:17pm GMT+0100'\n\t\t\t\t\tStaticText '2 years ago'\n\t\t\t[595] listitem ''\n\t\t\t\t[600] link '[Feature suggestion] WCAG trash panda mode', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/issues/39'\n\t\t\t\tStaticText '1 of 3 checklist items completed'\n\t\t\t\tStaticText 'byteblaze/a11y-webring.club#39'\n\t\t\t\tStaticText '\u00b7 created'\n\t\t\t\t[605] time 'Jan 22, 2023 7:23pm UTC'\n\t\t\t\t\tStaticText '2 years ago'\n\t\t\t\tStaticText 'by'\n\t\t\t\t[606] link 'Byte Blaze', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze'\n\t\t\t\t\tStaticText 'Byte Blaze'\n\t\t\t\tStaticText ''\n\t\t\t\t[609] link 'feature', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/issues?label_name%5B%5D=feature'\n\t\t\t\t\tStaticText 'feature'\n\t\t\t\t[612] link 'help wanted', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/issues?label_name%5B%5D=help+wanted'\n\t\t\t\t\tStaticText 'help wanted'\n\t\t\t\t[615] list ''\n\t\t\t\t\t[616] listitem ''\n\t\t\t\t\t\t[617] link 'Assigned to Byte Blaze', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze'\n\t\t\t\t\t\t\t[618] image '', url='https://www.gravatar.com/avatar/99a4297c867eada2606b9b6973f081f9?s=32&d=identicon'\n\t\t\t\t\t[619] listitem ''\n\t\t\t\t\t\t[620] link '0', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/issues/39#notes'\n\t\t\t\t\t\t\t[621] image ''\n\t\t\t\tStaticText 'updated'\n\t\t\t\t[624] time 'Mar 27, 2023 9:17pm GMT+0100'\n\t\t\t\t\tStaticText '2 years ago'\n\t\t\t[625] listitem ''\n\t\t\t\t[630] link '[Feature suggestion] Add a submission form', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/issues/30'\n\t\t\t\tStaticText '1 of 3 checklist items completed'\n\t\t\t\tStaticText 'byteblaze/a11y-webring.club#30'\n\t\t\t\tStaticText '\u00b7 created'\n\t\t\t\t[635] time 'Jan 20, 2023 8:16pm UTC'\n\t\t\t\t\tStaticText '2 years ago'\n\t\t\t\tStaticText 'by'\n\t\t\t\t[636] link 'Byte Blaze', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze'\n\t\t\t\t\tStaticText 'Byte Blaze'\n\t\t\t\tStaticText ''\n\t\t\t\t[639] link 'feature', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/issues?label_name%5B%5D=feature'\n\t\t\t\t\tStaticText 'feature'\n\t\t\t\t[642] list ''\n\t\t\t\t\t[643] listitem ''\n\t\t\t\t\t\t[644] link 'Assigned to Byte Blaze', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze'\n\t\t\t\t\t\t\t[645] image '', url='https://www.gravatar.com/avatar/99a4297c867eada2606b9b6973f081f9?s=32&d=identicon'\n\t\t\t\t\t[646] listitem ''\n\t\t\t\t\t\t[647] link '0', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/issues/30#notes'\n\t\t\t\t\t\t\t[648] image ''\n\t\t\t\tStaticText 'updated'\n\t\t\t\t[651] time 'Mar 27, 2023 9:17pm GMT+0100'\n\t\t\t\t\tStaticText '2 years ago'\n\t\t\t[652] listitem ''\n\t\t\t\t[657] link '[Feature suggestion] Color theme slider', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/issues/21'\n\t\t\t\tStaticText '1 of 3 checklist items completed'\n\t\t\t\tStaticText 'byteblaze/a11y-webring.club#21'\n\t\t\t\tStaticText '\u00b7 created'\n\t\t\t\t[662] time 'Jan 19, 2023 3:58am UTC'\n\t\t\t\t\tStaticText '2 years ago'\n\t\t\t\tStaticText 'by'\n\t\t\t\t[663] link 'Byte Blaze', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze'\n\t\t\t\t\tStaticText 'Byte Blaze'\n\t\t\t\tStaticText ''\n\t\t\t\t[666] link 'feature', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/issues?label_name%5B%5D=feature'\n\t\t\t\t\tStaticText 'feature'\n\t\t\t\t[669] link 'help wanted', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/issues?label_name%5B%5D=help+wanted'\n\t\t\t\t\tStaticText 'help wanted'\n\t\t\t\t[672] list ''\n\t\t\t\t\t[673] listitem ''\n\t\t\t\t\t\t[674] link 'Assigned to Byte Blaze', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze'\n\t\t\t\t\t\t\t[675] image '', url='https://www.gravatar.com/avatar/99a4297c867eada2606b9b6973f081f9?s=32&d=identicon'\n\t\t\t\t\t[676] listitem ''\n\t\t\t\t\t\t[677] link '0', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/issues/21#notes'\n\t\t\t\t\t\t\t[678] image ''\n\t\t\t\tStaticText 'updated'\n\t\t\t\t[681] time 'Mar 27, 2023 9:17pm GMT+0100'\n\t\t\t\t\tStaticText '2 years ago'\n\t\t\t[682] listitem ''\n\t\t\t\t[687] link 'Link to WCAG 2.1 instead of 2.0?', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/a11yproject/a11yproject.com/-/issues/1460'\n\t\t\t\tStaticText 'a11yproject/a11yproject.com#1460'\n\t\t\t\tStaticText '\u00b7 created'\n\t\t\t\t[691] time 'Aug 11, 2022 5:10pm GMT+0100'\n\t\t\t\t\tStaticText '2 years ago'\n\t\t\t\tStaticText 'by'\n\t\t\t\t[692] link 'Byte Blaze', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze'\n\t\t\t\t\tStaticText 'Byte Blaze'\n\t\t\t\tStaticText ''\n\t\t\t\t[695] link 'claimed', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/a11yproject/a11yproject.com/-/issues?label_name%5B%5D=claimed'\n\t\t\t\t\tStaticText 'claimed'\n\t\t\t\t[698] link 'content', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/a11yproject/a11yproject.com/-/issues?label_name%5B%5D=content'\n\t\t\t\t\tStaticText 'content'\n\t\t\t\t[701] list ''\n\t\t\t\t\t[702] listitem ''\n\t\t\t\t\t\t[703] link 'Assigned to Byte Blaze', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze'\n\t\t\t\t\t\t\t[704] image '', url='https://www.gravatar.com/avatar/99a4297c867eada2606b9b6973f081f9?s=32&d=identicon'\n\t\t\t\t\t[705] listitem ''\n\t\t\t\t\t\t[706] link '0', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/a11yproject/a11yproject.com/-/issues/1460#notes'\n\t\t\t\t\t\t\t[707] image ''\n\t\t\t\tStaticText 'updated'\n\t\t\t\t[710] time 'Mar 23, 2023 8:42am UTC'\n\t\t\t\t\tStaticText '2 years ago'\n\t\t\t[711] listitem ''\n\t\t\t\t[716] link 'The process for writing for us is both scattered and buried', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/a11yproject/a11yproject.com/-/issues/1360'\n\t\t\t\tStaticText 'a11yproject/a11yproject.com#1360'\n\t\t\t\tStaticText '\u00b7 created'\n\t\t\t\t[720] time 'Oct 11, 2021 1:35am GMT+0100'\n\t\t\t\t\tStaticText '3 years ago'\n\t\t\t\tStaticText 'by'\n\t\t\t\t[721] link 'Byte Blaze', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze'\n\t\t\t\t\tStaticText 'Byte Blaze'\n\t\t\t\tStaticText ''\n\t\t\t\t[724] link 'content', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/a11yproject/a11yproject.com/-/issues?label_name%5B%5D=content'\n\t\t\t\t\tStaticText 'content'\n\t\t\t\t[727] link 'design', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/a11yproject/a11yproject.com/-/issues?label_name%5B%5D=design'\n\t\t\t\t\tStaticText 'design'\n\t\t\t\t[730] list ''\n\t\t\t\t\t[731] listitem ''\n\t\t\t\t\t\t[732] link 'Assigned to Byte Blaze', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze'\n\t\t\t\t\t\t\t[733] image '', url='https://www.gravatar.com/avatar/99a4297c867eada2606b9b6973f081f9?s=32&d=identicon'\n\t\t\t\t\t[734] listitem ''\n\t\t\t\t\t\t[735] link '2', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/a11yproject/a11yproject.com/-/issues/1360#notes'\n\t\t\t\t\t\t\t[736] image ''\n\t\t\t\tStaticText 'updated'\n\t\t\t\t[739] time 'Mar 23, 2023 8:41am UTC'\n\t\t\t\t\tStaticText '2 years ago'\n\t\t\t[740] listitem ''\n\t\t\t\t[745] link 'Non-Github contribution guidelines need clarification', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/a11yproject/a11yproject.com/-/issues/1294'\n\t\t\t\tStaticText 'a11yproject/a11yproject.com#1294'\n\t\t\t\tStaticText '\u00b7 created'\n\t\t\t\t[749] time 'Jun 17, 2021 3:18am GMT+0100'\n\t\t\t\t\tStaticText '3 years ago'\n\t\t\t\tStaticText 'by'\n\t\t\t\t[750] link 'Byte Blaze', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze'\n\t\t\t\t\tStaticText 'Byte Blaze'\n\t\t\t\tStaticText ''\n\t\t\t\t[753] link 'claimed', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/a11yproject/a11yproject.com/-/issues?label_name%5B%5D=claimed'\n\t\t\t\t\tStaticText 'claimed'\n\t\t\t\t[756] link 'content', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/a11yproject/a11yproject.com/-/issues?label_name%5B%5D=content'\n\t\t\t\t\tStaticText 'content'\n\t\t\t\t[759] list ''\n\t\t\t\t\t[760] listitem ''\n\t\t\t\t\t\t[761] link 'Assigned to Byte Blaze', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze'\n\t\t\t\t\t\t\t[762] image '', url='https://www.gravatar.com/avatar/99a4297c867eada2606b9b6973f081f9?s=32&d=identicon'\n\t\t\t\t\t[763] listitem ''\n\t\t\t\t\t\t[764] link '2', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/a11yproject/a11yproject.com/-/issues/1294#notes'\n\t\t\t\t\t\t\t[765] image ''\n\t\t\t\tStaticText 'updated'\n\t\t\t\t[768] time 'Mar 23, 2023 8:41am UTC'\n\t\t\t\t\tStaticText '2 years ago'\n\t\t\t[769] listitem ''\n\t\t\t\t[774] link 'Outdated dependencies', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/empathy-prompts/-/issues/18'\n\t\t\t\tStaticText 'byteblaze/empathy-prompts#18'\n\t\t\t\tStaticText '\u00b7 created'\n\t\t\t\t[778] time 'Jun 2, 2021 1:52am GMT+0100'\n\t\t\t\t\tStaticText '3 years ago'\n\t\t\t\tStaticText 'by'\n\t\t\t\t[779] link 'Byte Blaze', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze'\n\t\t\t\t\tStaticText 'Byte Blaze'\n\t\t\t\tStaticText ''\n\t\t\t\t[782] link '[Priority] Critical', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/empathy-prompts/-/issues?label_name%5B%5D=%5BPriority%5D+Critical'\n\t\t\t\t\tStaticText '[Priority] Critical'\n\t\t\t\t[785] link '[Status] Submitted', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/empathy-prompts/-/issues?label_name%5B%5D=%5BStatus%5D+Submitted'\n\t\t\t\t\tStaticText '[Status] Submitted'\n\t\t\t\t[788] link '[Type] Bug', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/empathy-prompts/-/issues?label_name%5B%5D=%5BType%5D+Bug'\n\t\t\t\t\tStaticText '[Type] Bug'\n\t\t\t\t[791] list ''\n\t\t\t\t\t[792] listitem ''\n\t\t\t\t\t\t[793] link 'Assigned to Byte Blaze', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze'\n\t\t\t\t\t\t\t[794] image '', url='https://www.gravatar.com/avatar/99a4297c867eada2606b9b6973f081f9?s=32&d=identicon'\n\t\t\t\t\t[795] listitem ''\n\t\t\t\t\t\t[796] link '0', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/empathy-prompts/-/issues/18#notes'\n\t\t\t\t\t\t\t[797] image ''\n\t\t\t\tStaticText 'updated'\n\t\t\t\t[800] time 'Mar 27, 2023 9:16pm GMT+0100'\n\t\t\t\t\tStaticText '2 years ago'\n\t\t\t[801] listitem ''\n\t\t\t\t[806] link 'Inaccessibility: Low contrast .c-card__additional in Featured Resource Card', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/a11yproject/a11yproject.com/-/issues/1208'\n\t\t\t\tStaticText 'a11yproject/a11yproject.com#1208'\n\t\t\t\tStaticText '\u00b7 created'\n\t\t\t\t[810] time 'Mar 12, 2021 3:56pm UTC'\n\t\t\t\t\tStaticText '4 years ago'\n\t\t\t\tStaticText 'by'\n\t\t\t\t[811] link 'Administrator', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/root'\n\t\t\t\t\tStaticText 'Administrator'\n\t\t\t\tStaticText ''\n\t\t\t\t[814] link 'accessibility', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/a11yproject/a11yproject.com/-/issues?label_name%5B%5D=accessibility'\n\t\t\t\t\tStaticText 'accessibility'\n\t\t\t\t[817] link 'resource', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/a11yproject/a11yproject.com/-/issues?label_name%5B%5D=resource'\n\t\t\t\t\tStaticText 'resource'\n\t\t\t\t[820] link 'styling', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/a11yproject/a11yproject.com/-/issues?label_name%5B%5D=styling'\n\t\t\t\t\tStaticText 'styling'\n\t\t\t\t[823] list ''\n\t\t\t\t\t[824] listitem ''\n\t\t\t\t\t\t[825] link 'Assigned to Byte Blaze', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze'\n\t\t\t\t\t\t\t[826] image '', url='https://www.gravatar.com/avatar/99a4297c867eada2606b9b6973f081f9?s=32&d=identicon'\n\t\t\t\t\t[827] listitem ''\n\t\t\t\t\t\t[828] link '7', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/a11yproject/a11yproject.com/-/issues/1208#notes'\n\t\t\t\t\t\t\t[829] image ''\n\t\t\t\tStaticText 'updated'\n\t\t\t\t[832] time 'Mar 23, 2023 8:41am UTC'\n\t\t\t\t\tStaticText '2 years ago'\n\t\t\t[833] listitem ''\n\t\t\t\t[838] link 'Tm Theme Editor', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-syntax-highlighting/-/issues/1'\n\t\t\t\tStaticText 'byteblaze/a11y-syntax-highlighting#1'\n\t\t\t\tStaticText '\u00b7 created'\n\t\t\t\t[842] time 'Apr 2, 2020 5:13am GMT+0100'\n\t\t\t\t\tStaticText '5 years ago'\n\t\t\t\tStaticText 'by'\n\t\t\t\t[843] link 'earle', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/earlev4'\n\t\t\t\t\tStaticText 'earle'\n\t\t\t\t[846] list ''\n\t\t\t\t\t[847] listitem ''\n\t\t\t\t\t\t[848] link 'Assigned to Byte Blaze', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze'\n\t\t\t\t\t\t\t[849] image '', url='https://www.gravatar.com/avatar/99a4297c867eada2606b9b6973f081f9?s=32&d=identicon'\n\t\t\t\t\t[850] listitem ''\n\t\t\t\t\t\t[851] link '14', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-syntax-highlighting/-/issues/1#notes'\n\t\t\t\t\t\t\t[852] image ''\n\t\t\t\tStaticText 'updated'\n\t\t\t\t[855] time 'Mar 28, 2023 12:15am GMT+0100'\n\t\t\t\t\tStaticText '2 years ago'\n\t\t\t[856] listitem ''\n\t\t\t\t[861] link 'Empathy Balloons', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/empathy-prompts/-/issues/10'\n\t\t\t\tStaticText 'byteblaze/empathy-prompts#10'\n\t\t\t\tStaticText '\u00b7 created'\n\t\t\t\t[865] time 'Jun 21, 2019 11:37am GMT+0100'\n\t\t\t\t\tStaticText '5 years ago'\n\t\t\t\tStaticText 'by'\n\t\t\t\t[866] link 'Rik Williams', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/rik-williams'\n\t\t\t\t\tStaticText 'Rik Williams'\n\t\t\t\tStaticText ''\n\t\t\t\t[869] link '[Priority] Low', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/empathy-prompts/-/issues?label_name%5B%5D=%5BPriority%5D+Low'\n\t\t\t\t\tStaticText '[Priority] Low'\n\t\t\t\t[872] link '[Status] Accepted', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/empathy-prompts/-/issues?label_name%5B%5D=%5BStatus%5D+Accepted'\n\t\t\t\t\tStaticText '[Status] Accepted'\n\t\t\t\t[875] link '[Type] Enhancement', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/empathy-prompts/-/issues?label_name%5B%5D=%5BType%5D+Enhancement'\n\t\t\t\t\tStaticText '[Type] Enhancement'\n\t\t\t\t[878] list ''\n\t\t\t\t\t[879] listitem ''\n\t\t\t\t\t\t[880] link 'Assigned to Byte Blaze', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze'\n\t\t\t\t\t\t\t[881] image '', url='https://www.gravatar.com/avatar/99a4297c867eada2606b9b6973f081f9?s=32&d=identicon'\n\t\t\t\t\t[882] listitem ''\n\t\t\t\t\t\t[883] link '2', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/empathy-prompts/-/issues/10#notes'\n\t\t\t\t\t\t\t[884] image ''\n\t\t\t\tStaticText 'updated'\n\t\t\t\t[887] time 'Mar 27, 2023 9:16pm GMT+0100'\n\t\t\t\t\tStaticText '2 years ago'\n\t\t\t[888] listitem ''\n\t\t\t\t[893] link 'Better initial load experience', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/empathy-prompts/-/issues/8'\n\t\t\t\tStaticText 'byteblaze/empathy-prompts#8'\n\t\t\t\tStaticText '\u00b7 created'\n\t\t\t\t[897] time 'May 18, 2017 3:29am GMT+0100'\n\t\t\t\t\tStaticText '7 years ago'\n\t\t\t\tStaticText 'by'\n\t\t\t\t[898] link 'Byte Blaze', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze'\n\t\t\t\t\tStaticText 'Byte Blaze'\n\t\t\t\tStaticText ''\n\t\t\t\t[901] link '[Priority] Low', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/empathy-prompts/-/issues?label_name%5B%5D=%5BPriority%5D+Low'\n\t\t\t\t\tStaticText '[Priority] Low'\n\t\t\t\t[904] link '[Status] Submitted', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/empathy-prompts/-/issues?label_name%5B%5D=%5BStatus%5D+Submitted'\n\t\t\t\t\tStaticText '[Status] Submitted'\n\t\t\t\t[907] link '[Type] Enhancement', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/empathy-prompts/-/issues?label_name%5B%5D=%5BType%5D+Enhancement'\n\t\t\t\t\tStaticText '[Type] Enhancement'\n\t\t\t\t[910] list ''\n\t\t\t\t\t[911] listitem ''\n\t\t\t\t\t\t[912] link 'Assigned to Byte Blaze', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze'\n\t\t\t\t\t\t\t[913] image '', url='https://www.gravatar.com/avatar/99a4297c867eada2606b9b6973f081f9?s=32&d=identicon'\n\t\t\t\t\t[914] listitem ''\n\t\t\t\t\t\t[915] link '0', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/empathy-prompts/-/issues/8#notes'\n\t\t\t\t\t\t\t[916] image ''\n\t\t\t\tStaticText 'updated'\n\t\t\t\t[919] time 'Mar 27, 2023 9:16pm GMT+0100'\n\t\t\t\t\tStaticText '2 years ago'\n\t\t\t[920] listitem ''\n\t\t\t\t[925] link 'Better sharing solution', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/empathy-prompts/-/issues/6'\n\t\t\t\tStaticText 'byteblaze/empathy-prompts#6'\n\t\t\t\tStaticText '\u00b7 created'\n\t\t\t\t[929] time 'May 5, 2017 2:31am GMT+0100'\n\t\t\t\t\tStaticText '7 years ago'\n\t\t\t\tStaticText 'by'\n\t\t\t\t[930] link 'Byte Blaze', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze'\n\t\t\t\t\tStaticText 'Byte Blaze'\n\t\t\t\tStaticText ''\n\t\t\t\t[933] link '[Priority] Medium', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/empathy-prompts/-/issues?label_name%5B%5D=%5BPriority%5D+Medium'\n\t\t\t\t\tStaticText '[Priority] Medium'\n\t\t\t\t[936] link '[Status] Submitted', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/empathy-prompts/-/issues?label_name%5B%5D=%5BStatus%5D+Submitted'\n\t\t\t\t\tStaticText '[Status] Submitted'\n\t\t\t\t[939] link '[Type] Enhancement', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/empathy-prompts/-/issues?label_name%5B%5D=%5BType%5D+Enhancement'\n\t\t\t\t\tStaticText '[Type] Enhancement'\n\t\t\t\t[942] list ''\n\t\t\t\t\t[943] listitem ''\n\t\t\t\t\t\t[944] link 'Assigned to Byte Blaze', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze'\n\t\t\t\t\t\t\t[945] image '', url='https://www.gravatar.com/avatar/99a4297c867eada2606b9b6973f081f9?s=32&d=identicon'\n\t\t\t\t\t[946] listitem ''\n\t\t\t\t\t\t[947] link '2', url='http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/empathy-prompts/-/issues/6#notes'\n\t\t\t\t\t\t\t[948] image ''\n\t\t\t\tStaticText 'updated'\n\t\t\t\t[951] time 'Mar 27, 2023 9:16pm GMT+0100'\n\t\t\t\t\tStaticText '2 years ago'\n\t[1015] status '', live='polite', atomic, relevant='additions text'\n\t\tStaticText '14 results are available, use up and down arrow keys to navigate.'\n\t[253] LabelText ''\n\t[254] combobox '', focused, autocomplete='list', hasPopup='listbox', expanded=True, owns='select2-results-1', controls=''\n\t[255] listbox '', multiselectable=False, orientation='vertical'\n\t\t[1046] option 'The A11Y Project / a11yproject.com', selected=True\n\t\t[1049] option 'Byte Blaze / solarized-prism-theme', selected=False\n\t\t[1052] option 'Byte Blaze / gimmiethat.space', selected=False\n\t\t[1055] option 'Byte Blaze / dotfiles', selected=False\n\t\t[1058] option 'Byte Blaze / timeit', selected=False\n\t\t[1061] option 'Byte Blaze / cloud-to-butt', selected=False\n\t\t[1064] option 'Byte Blaze / millennials-to-snake-people', selected=False\n\t\t[1067] option 'Byte Blaze / a11y-syntax-highlighting', selected=False\n\t\t[1070] option 'Byte Blaze / accessible-html-content-patterns', selected=False\n\t\t[1073] option 'Byte Blaze / empathy-prompts', selected=False\n\t\t[1076] option 'Byte Blaze / ericwbailey.website', selected=False\n\t\t[1079] option 'Byte Blaze / remove-board-movement-events-from-the-github-issue-timeline', selected=False\n\t\t[1082] option 'Primer / design', selected=False\n\t\t[1085] option 'Byte Blaze / a11y-webring.club', selected=False
"""

obj = """
FilterAndSort [help wanted]
"""

task_name = """
FilterAndSort
"""

query = """
help wanted
"""

description = """
Filter and sort the issues on the issues page by a given criteria.
"""


url = """
http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/byteblaze/a11y-webring.club/-/issues/?sort=title_asc&state=opened&label_name%5B%5D=help%20wanted&first_page_size=20
"""

# get_critique(obj, init_obs, "", previous_actions, init_obs)



breakdown = """
1. Type 'help wanted' in the textbox to filter the issues.
2. Click the combobox.
3. Click the "Priority" button (multiple redundant clicks).
4. Click the "Sort direction" link.
5. Click the "Toggle project select" button.
6. Click the "Author" button (multiple redundant clicks).
7. Click different project options in the combobox.
8. Click "Created date" option in the listbox.
9. Click "help wanted" link.
10. Click "Created date" button.
11. Click the "Title" sorting option to sort issues by title.
12. Click the "Sort direction: Ascending" button to sort ascending.*
"""

# feedback = """
# The task is a success because the issues are filtered by 'help wanted' and sorted by title ascending. The URL confirms that `sort=title_asc` and `label_name[]=help%20wanted` parameters are present. While several actions were redundant or unnecessary, the final state fulfills the objective.
# """

feedback = """
The task is a success because the issues are filtered by 'help wanted' and sorted by title ascending. The URL confirms that `sort=title_asc` and `label_name[]=help%20wanted` parameters are present. Here are the main actions that lead to a success :
1. Click on the link with the text "help wanted" to filter the issues.
2. Click on the "Title" button to open the sorting options.
3. Select the "Title" option to sort by title.
4. Ensure that the sort direction is set to ascending by clicking the "Sort direction" button until it displays "Sort direction: Ascending".
"""


# old_guidance = """
# Locate the column header (e.g., \"Updated date\") corresponding to the desired sorting criteria.\n*   Click the column header to sort by that criteria. The first click typically sorts in ascending order.\n*   If the desired sort direction is descending, click the *same* column header again to toggle the sort direction.\n*   Stop once the issues are sorted by the specified criteria and in the correct direction. Avoid unnecessary clicks after the desired sorting is achieved.
# """

# old_guidance = """

# """


# write_policy(task_name, description, query, obs, breakdown, feedback, old_guidance, init_obs)

# REVIEW: The navigation started on the issues dashboard. Several attempts were made to open the sorting menu using the "Priority" button, "Sort direction" link, and other interactive elements, but without success. A combobox with project options was clicked. Finally, the issues are filtered by the label "help wanted" by clicking on the 'help wanted' link. After this, the "Title" sort was selected and the sort direction was set to ascending.
# EXPLAIN: The objective was to filter issues by the "help wanted" label and sort them by title in ascending order. The current URL indicates that the issues are indeed filtered by "help wanted" (label_name%5B%5D=help%20wanted) and sorted by title in ascending order (sort=title_asc). Therefore, the objective has been successfully fulfilled.
# SUCCESS: 1
# FEEDBACK:
# 1. Click on the link with the text "help wanted" to filter the issues.
# 2. Click on the "Title" button to open the sorting options.
# 3. Select the "Title" option to sort by title.
# 4. Ensure that the sort direction is set to ascending by clicking the "Sort direction" button until it displays "Sort direction: Ascending".



print(generate_content("Hello world"))