# Functions to quickly test the prompts of the different components :
from writing_policy import get_my_writing_answer
from get_action import get_my_action
from critique import get_my_critique
from get_policy import get_my_policy
from policy_library import PolicyLibrary
from utils import *
from web_environment import WebEnvironment, AvailableURL, print_gym_call


# print(AvailableURL.REDDIT.value)

# print(print_gym_call("go_back", ['42', "Carnegie"]))

env = WebEnvironment()
env.load(AvailableURL.REDDIT.value)
print(env.observe())
env.interact("click", ["310"])
print(env.observe())
env.interact("go_home", [])
print(env.observe())

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