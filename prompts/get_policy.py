from utils import *


policies = """
 `find_commits [query]`: Given you are in a project page, this Gitlab subroutine searches for commits made to the project and retrieves information about a commit. This function returns the answer to the query.
 `find_subreddit [query]`: This Reddit subroutine finds a subreddit corresponding to the query. The query can either be the name of the subreddit or a vague description of what the subreddit may contain. The subroutine hands back control once it navigates to the subreddit.
 `search_customer [query]`: This CMS subroutine finds a customer given some details about them such as their phone number.
 `search_reviews [query]`: This Shopping subroutine searches reviews to answer a question about reviews.
 `find_directions [query]`: This Maps subroutine finds directions between two locations to answer the query.
 """

example_actions = """
find_commits [How many commits did user make to diffusionProject on 03/23/2023?]
search_issues [Open my latest updated issue that has keyword "better" in its title to check if it is closed]
create_project [Create a new public project "awesome-llms" and add primer, convexegg, abishek as members]
create_group [Create a new group "coding_friends" with members qhduan, Agnes-U]
find_subreddit [books]
find_user [AdamCannon]
find_customer_review [Show me customer reviews for Zoe products]
find_order [Most recent pending order by Sarah Miller]
search_customer [Search customer with phone number 8015551212]
search_order [How much I spend on 4/19/2023 on shopping at One Stop Market?]
list_products [List products from PS4 accessories category by ascending price]
search_reviews [List out reviewers, if exist, who mention about ear cups being small]
find_directions [Check if the social security administration in Pittsburgh can be reached in one hour by car from Carnegie Mellon University]
search_nearest_place [Tell me the closest cafe(s) to CMU Hunt library]
"""



get_policy_system_prompt = """
You are an AI assistant calling subroutine to perform tasks on a web browser.
You will divide your objective into subtasks and call specific functions or subroutines to solve these subtasks.


Here some example of subroutines along with their descriptions :
{policies}

Here are the afromentionned example subroutines called with their associated queries :
{example_actions}

You will be provided with the following,
OBJECTIVE:
The goal you need to achieve.
OBSERVATION:
A simplified text description of the current browser content, without formatting elements.
URL:
The current webpage URL
SUBROUTINES:
The available subroutines at your disposal.


You should call one of the available subroutines along with the right query to solve the subtasks (see example subroutines for how to call them).
If none of the available subroutines fit the subtask, you can create and call a new subroutine by simply providing its name and description.


You should then respond to me with :
Plan: Divide the objective into at most 2 clear and equally complex subtasks starting from the observation. The subtasks should be general and abstract away the specifics of the website. Your plan should contain the smallest possible number of subtasks.
For each of the following categories, you need to provide an answer for each corresponding subtask in your plan separated by |
Name: The names of the subroutines you want to call to solve each subtask (subtroutine_name_1 | subtroutine_name_1 | ...)
Description: The descriptions of the subroutines you want to call. (description_1 | description_2 | ...)
Query: The argument with which each subroutine will be called. (query_1 | query_2 | ...)

Here are some general guidelines to keep in mind :
1. You do not have access to external ressources. Limit yourself to the content of the current webpage.
2. Subroutines should be generic and only depends on the type of website your in and not the website itself.
3. If you create a subroutine, the name of the newly created subroutine should match the current subtask.
4. Subroutines shouldn't be too simple : they should be an abstraction of at least two page operations.

Please issue only a single action at a time.
Adhere strictly to the following output format :
RESPONSE FORMAT :
PLAN: ...
NAME: ...
DESCRIPTION: ...
QUERY: ...
"""


def get_policy(objective, observation, url, relevant_policies):
    get_policy_prompt = f"""
    {get_policy_system_prompt}

    OBJECTIVE: {objective}
    OBSERVATION: {observation}
    URL: {url}
    SUBROUTINES: {[f"{name} [query] : {description}" for (name, description) in relevant_policies]}
    """


    answer = generate_content(get_policy_prompt)

    result = parse_elements(answer, ["plan", "name", "description", "query"])

            
    names = result["name"].split(" | ")
    descriptions = result["description"].split(" | ")
    queries = result["query"].split(" | ")

    policies = [{"name": name, "description": desc, "query": query} for name, desc, query in zip(names, descriptions, queries)]
 

    return {"plan" : result["plan"], "policies" : policies}
