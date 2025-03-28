from utils import *


policies = """
`findCommits [query]`: Given you are in a project page, this Gitlab subroutine searches for commits made to the project and retrieves information about a commit. This function returns the answer to the query.
`findSubreddit [query]`: This Reddit subroutine finds a subreddit corresponding to the query. The query can either be the name of the subreddit or a vague description of what the subreddit may contain. The subroutine hands back control once it navigates to the subreddit.
`searchCustomer [query]`: This CMS subroutine finds a customer given some details about them such as their phone number.
`searchReviews [query]`: This Shopping subroutine searches reviews to answer a question about reviews.
`findDirections [query]`: This Maps subroutine finds directions between two locations to answer the query.
"""

example_actions = """
findCommits [How many commits did user make to diffusionProject on 03/23/2023?]
searchIssues [Open my latest updated issue that has keyword "better" in its title to check if it is closed]
createProject [Create a new public project "awesome-llms" and add primer, convexegg, abishek as members]
createGroup [Create a new group "coding_friends" with members qhduan, Agnes-U]
findSubreddit [books]
findUser [AdamCannon]
findCustomer_review [Show me customer reviews for Zoe products]
findOrder [Most recent pending order by Sarah Miller]
searchCustomer [Search customer with phone number 8015551212]
searchOrder [How much I spend on 4/19/2023 on shopping at One Stop Market?]
listProducts [List products from PS4 accessories category by ascending price]
searchReviews [List out reviewers, if exist, who mention about ear cups being small]
findDirections [Check if the social security administration in Pittsburgh can be reached in one hour by car from Carnegie Mellon University]
searchNearest_place [Tell me the closest cafe(s) to CMU Hunt library]
"""



get_policy_system_prompt = """
You are an AI assistant calling subroutine to perform tasks on a web browser.
You will divide your objective into subtasks and call specific functions or subroutines to solve these subtasks.


Here some example of subroutines actions along with their descriptions :
{policies}

Here are some example actions, either page operation or subroutine call :
{example_actions}

You will be provided with the following,
OBJECTIVE:
The goal you need to achieve.
OBSERVATION:
A simplified text description of the current browser content, without formatting elements.
URL:
The current webpage URL
PREVIOUS ACTIONS:
A list of your past actions with an optional response
SUBROUTINES:
The available subroutines at your disposal.
NEW:
Output 0 if you used one of the avilable subroutines at your disposal and 1 if you created the subroutine.


You should call one of the avilable subroutines along with the right argument to solve the subtask (see example subroutines for how to call them).
If none of the availble subroutines fit the subtask, you can create and call a new subroutine by simply providing its name and description.

 
You should then respond to me with :
Plan : Divide the objective into clear subtasks starting from the observation.
First Subtask : Clearly identify the first subtask of your plan and how to tackle it. If you think that the objective is completed, detail the answer to the objective if applicable.
Name : The name of the subroutine you want to call. Call stop if you think the objective is completed.
Description : The description of the subroutine you want to call.
Query : The argument with which the subroutine will be called. If the subroutine is stop, put here the answer to the objective here if applicable and nothing otherwise.

Here are some general guidelines to keep in mind :
1. A subroutine is a high-level function used to perform long-range tasks. A subroutine serves as an abstraction of multiple page operations.
2. You do not have access to external ressources. Limit yourself to the content of the current webpage.

You need to generate a response in the following format.
Please issue only a single action at a time.
RESPONSE FORMAT :
PLAN: ...
SUBTASK: ...
NAME: ...
DESCRIPTION: ...
QUERY: ...
NEW: ...
"""


def get_policy(objective, observation, url, previous_actions, relevant_policies):
    get_policy_prompt = f"""
    {get_policy_system_prompt}
    OBJECTIVE: {objective}
    OBSERVATION: {observation}
    URL: {url}
    PREVIOUS ACTIONS: {previous_actions}
    SUBROUTINES: {[f"{name} [query] : {description}" for (name, description) in relevant_policies] + ["stop [answer]"]}
    """


    answer = generate_content(get_policy_prompt)

    result = parse_elements(answer, ["plan", "subtask", "name", "description", "query", "new"])


    return result


# ==== Prompt testing ===


my_objective = """
Tell me the full address of all international airports that are within a driving distance of 30 km to Carnegie Art Museum
"""

my_observation = """
Tab 0 (current): OpenStreetMap\n\n[1] RootWebArea 'OpenStreetMap' focused: True\n\t[36] heading 'OpenStreetMap logo OpenStreetMap'\n\t\t[41] link 'OpenStreetMap logo OpenStreetMap'\n\t\t\t[44] img 'OpenStreetMap logo'\n\t[402] link 'Edit'\n\t[403] button ''\n\t[373] link 'History'\n\t[374] link 'Export'\n\t[407] link 'GPS Traces'\n\t[408] link 'User Diaries'\n\t[409] link 'Communities'\n\t[410] link 'Copyright'\n\t[411] link 'Help'\n\t[412] link 'About'\n\t[382] link 'Log In'\n\t[383] link 'Sign Up'\n\t[515] link 'Where is this?'\n\t[12] textbox 'Search' focused: True required: False\n\t[516] button 'Go'\n\t[503] link 'Find directions between two points'\n\t[466] heading 'Welcome to OpenStreetMap!'\n\t[469] button 'Close'\n\t[473] StaticText 'OpenStreetMap is a map of the world, created by people like you and free to use under an open license.'\n\t[474] StaticText 'Hosting is supported by '\n\t[475] link 'UCL'\n\t[477] link 'Fastly'\n\t[478] StaticText ', '\n\t[479] link 'Bytemark Hosting'\n\t[480] StaticText ', and other '\n\t[481] link 'partners'\n\t[482] StaticText '.'\n\t[485] link 'Learn More'\n\t[486] link 'Start Mapping'\n\t[23] generic 'Zoom In Zoom Out Show My Location Layers Share 50 km 50 mi \u00a9 OpenStreetMap contributors \u2665 Make a Donation. Website and API terms'\n\t\t[27] link 'Zoom In'\n\t\t[28] link 'Zoom Out'\n\t\t[30] button 'Show My Location'\n\t\t[32] link 'Layers'\n\t\t[296] link ''\n\t\t[34] link 'Share'\n\t\t[298] link ''\n\t\t[300] link ''\n\t\t[305] StaticText '50 km'\n\t\t[306] StaticText '50 mi'\n\t\t[308] StaticText '\u00a9 '\n\t\t[309] link 'OpenStreetMap contributors'\n\t\t[310] StaticText ' \u2665 '\n\t\t[311] link 'Make a Donation'\n\t\t[312] StaticText '. '\n\t\t[313] link 'Website and API terms'
"""

my_url = """
http://ec2-3-131-244-37.us-east-2.compute.amazonaws.com:3000/#map=7/42.896/-75.108
"""

my_previous_actions = """
"""

# my_relevant_policies = [
# ("find_directions", "This Maps subroutine finds directions between two locations to answer the query."),
# ("search_nearest_place", "This Maps subroutine finds places near a given location.")
# ]

my_relevant_policies = [
]


def get_my_policy():
    return get_policy(my_objective, my_observation, my_url, my_previous_actions, my_relevant_policies)