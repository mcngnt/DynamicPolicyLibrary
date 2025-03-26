from utils import *


policies = """
`find_commits [query]`: Given you are in a project page, this Gitlab subroutine searches for commits made to the project and retrieves information about a commit. This function returns the answer to the query.
`find_subreddit [query]`: This Reddit subroutine finds a subreddit corresponding to the query. The query can either be the name of the subreddit or a vague description of what the subreddit may contain. The subroutine hands back control once it navigates to the subreddit.
`search_customer [query]`: This CMS subroutine finds a customer given some details about them such as their phone number.
`search_reviews [query]`: This Shopping subroutine searches reviews to answer a question about reviews.
`find_directions [query]`: This Maps subroutine finds directions between two locations to answer the query.
"""

example_actions = """
click [7]
type [15] [Carnegie Banana University] [1]
stop [Closed]
note [Spent $10 on 4/1/2024]
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

base_actions = """
- `click [id]`: To click on an element with its numerical ID on the webpage. E.g. , ‘click [7] ’ If clicking on a specific element doesn ’ t trigger the transition to your desired web state , this is due to the element’s lack of interactivity or GUI visibility . In such cases, move on to interact with OTHER similar or relevant elements INSTEAD.
- `type [id] [content] [press enter after = 0|1]`: To type content into a field with a specific ID. By default , the ‘ Enter ’ key is pressed after typing unless ‘press enter after ’ is set to 0. E.g. , ‘type [15] [Carnegie Mellon University ] [1] ’ If you can ’ t find what you’re looking for on your first attempt , consider refining your search keywords by breaking them down or trying related terms.
- `go_back` : To return to the previously viewed page.
- `note [content]`: To take note of all important info w.r.t. completing the task to enable reviewing it later . E.g. , ‘note [Spent $10 on 4/1/2024] ’
- `go_home`: To return to the homepage where you can find other websites.
- `stop [answer]`: To stop interaction and return response. Present your answer within the brackets . If the task doesn’t require a textual answer or appears insurmountable, indicate ‘N/A’ and additional reasons and all relevant information you gather as the answer . E.g. , ‘stop [5h 47min]’
"""



get_action_system_prompt = """
You are an AI assistant performing tasks on a web browser.
To solve these tasks, you will issue specific actions.

The actions you can perform fall into two categories:

1. Page Operation Actions:
{base_actions}

2. Subroutine Actions, here some example of subroutines actions with descriptions :
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
GUIDANCE TEXT:
A short text to guide you through the task-solving process.

 
You should then respond to me with :
Reason : Your reason for selecting the action
Action : The action you choose to perform in the format action_name [argument_1] ... [argument_n]
Description : If the action is a subroutine, describe the general expected behaviour of the subroutine, abstracting away the arguments with which it is called.

Here are some general guidelines to keep in mind :
1. A subroutine is a high-level function used to perform long-range tasks. A subroutine serves as an abstraction of multiple page operations.
2. You can create new subroutines as needed. To do so, simply describe the general expected behaviour of the subroutine. The subroutine shouldn't be too specific (like `find_repository_tetris_project`) nor too general (like `find`).
3. Only use a subroutine actions if needed. Page operations action are better for simple tasks.
4. You do not have access to external ressources. Limit yourself to the content of the current webpage.
5. The subroutine along with its query argument should be understandable without the description.

You need to generate a response in the following format.
Please issue only a single action at a time.
RESPONSE FORMAT :
REASON: ...
ACTION: ...
DECSRIPTION: ...
""" 


def get_action(objective, observation, url, previous_actions, guidance_text):
    get_action_prompt = f"""
    {get_action_system_prompt}
    OBJECTIVE: {objective}
    OBSERVATION: {observation}
    URL: {url}
    PREVIOUS ACTIONS: {previous_actions}
    GUIDANCE TEXT : {guidance_text}
    """


    answer = generate_content(get_action_prompt)

    result = parse_elements(answer, ["reason", "action", "description"])

    print("-------")
    print(objective)
    print(result)
    print("-----")

    arguments = parse_action_call(result["action"])

    is_atomic = arguments[0] in ["click", "type", "go_back", "note", "stop", "go_home"]

    action = {"name":arguments[0], "arguments":arguments[1:], "is_atomic":is_atomic, "description":result["description"]}

    return action


# ==== Prompt testing ===


my_objective = """
Tell me the full address of all international airports that are within a driving distance of 30 km to Carnegie Art Museum
"""

# my_observation = """
# Tab 0 (current): Carnegie Art Museum | OpenStreetMap\n\n[1] RootWebArea 'Carnegie Art Museum | OpenStreetMap' focused: True\n\t[36] heading 'OpenStreetMap logo OpenStreetMap'\n\t\t[41] link 'OpenStreetMap logo OpenStreetMap'\n\t\t\t[44] img 'OpenStreetMap logo'\n\t[402] link 'Edit'\n\t[403] button ''\n\t[373] link 'History'\n\t[374] link 'Export'\n\t[407] link 'GPS Traces'\n\t[408] link 'User Diaries'\n\t[409] link 'Communities'\n\t[410] link 'Copyright'\n\t[411] link 'Help'\n\t[412] link 'About'\n\t[382] link 'Log In'\n\t[383] link 'Sign Up'\n\t[12] textbox 'Search' focused: True required: False\n\t\t[522] StaticText 'Carnegie Art Museum'\n\t[516] button 'Go'\n\t[503] link 'Find directions between two points'\n\t[619] heading 'Search Results'\n\t[622] button 'Close'\n\t[617] heading 'Results from OpenStreetMap Nominatim'\n\t\t[624] link 'OpenStreetMap Nominatim'\n\t[631] StaticText 'Museum '\n\t[632] link 'Carnegie Museum of Art, South Craig Street, North Oakland, Pittsburgh, Allegheny County, 15213, United States'\n\t[629] link 'More results'\n\t[23] generic 'Zoom In Zoom Out Show My Location Layers Share 20 m 50 ft \u00a9 OpenStreetMap contributors \u2665 Make a Donation. Website and API terms'\n\t\t[27] link 'Zoom In'\n\t\t[28] link 'Zoom Out'\n\t\t[30] button 'Show My Location'\n\t\t[32] link 'Layers'\n\t\t[296] link ''\n\t\t[34] link 'Share'\n\t\t[298] link ''\n\t\t[300] link ''\n\t\t[614] StaticText '20 m'\n\t\t[615] StaticText '50 ft'\n\t\t[308] StaticText '\u00a9 '\n\t\t[309] link 'OpenStreetMap contributors'\n\t\t[310] StaticText ' \u2665 '\n\t\t[311] link 'Make a Donation'\n\t\t[312] StaticText '. '\n\t\t[313] link 'Website and API terms'
# """

my_observation = """
Tab 0 (current): OpenStreetMap\n\n[1] RootWebArea 'OpenStreetMap' focused: True\n\t[36] heading 'OpenStreetMap logo OpenStreetMap'\n\t\t[41] link 'OpenStreetMap logo OpenStreetMap'\n\t\t\t[44] img 'OpenStreetMap logo'\n\t[402] link 'Edit'\n\t[403] button ''\n\t[373] link 'History'\n\t[374] link 'Export'\n\t[407] link 'GPS Traces'\n\t[408] link 'User Diaries'\n\t[409] link 'Communities'\n\t[410] link 'Copyright'\n\t[411] link 'Help'\n\t[412] link 'About'\n\t[382] link 'Log In'\n\t[383] link 'Sign Up'\n\t[515] link 'Where is this?'\n\t[12] textbox 'Search' focused: True required: False\n\t[516] button 'Go'\n\t[503] link 'Find directions between two points'\n\t[466] heading 'Welcome to OpenStreetMap!'\n\t[469] button 'Close'\n\t[473] StaticText 'OpenStreetMap is a map of the world, created by people like you and free to use under an open license.'\n\t[474] StaticText 'Hosting is supported by '\n\t[475] link 'UCL'\n\t[477] link 'Fastly'\n\t[478] StaticText ', '\n\t[479] link 'Bytemark Hosting'\n\t[480] StaticText ', and other '\n\t[481] link 'partners'\n\t[482] StaticText '.'\n\t[485] link 'Learn More'\n\t[486] link 'Start Mapping'\n\t[23] generic 'Zoom In Zoom Out Show My Location Layers Share 50 km 50 mi \u00a9 OpenStreetMap contributors \u2665 Make a Donation. Website and API terms'\n\t\t[27] link 'Zoom In'\n\t\t[28] link 'Zoom Out'\n\t\t[30] button 'Show My Location'\n\t\t[32] link 'Layers'\n\t\t[296] link ''\n\t\t[34] link 'Share'\n\t\t[298] link ''\n\t\t[300] link ''\n\t\t[305] StaticText '50 km'\n\t\t[306] StaticText '50 mi'\n\t\t[308] StaticText '\u00a9 '\n\t\t[309] link 'OpenStreetMap contributors'\n\t\t[310] StaticText ' \u2665 '\n\t\t[311] link 'Make a Donation'\n\t\t[312] StaticText '. '\n\t\t[313] link 'Website and API terms'
"""

# my_url = """
# http://ec2-3-131-244-37.us-east-2.compute.amazonaws.com:3000/search?query=Carnegie%20Art%20Museum#map=19/40.44365/-79.94922
# """

my_url = """
http://ec2-3-131-244-37.us-east-2.compute.amazonaws.com:3000/#map=7/42.896/-75.108
"""

# my_previous_actions = """
# type [12] [Carnegie Art Museum] [1]
# """

my_previous_actions = """
"""


def get_my_action():
    return get_action(my_objective, my_observation, my_url, my_previous_actions)