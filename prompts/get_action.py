from utils import *



example_page_operation = """
click [7]
type [15] [Carnegie Banana University] [1]
go_home
stop [Closed]
note [Spent $10 on 4/1/2024]
stop [N/A]
type [789] [Best selling books] [0]
go_back
"""

page_operations = """
Page Operation Actions:
- `click [id]`: To click on an element with its numerical ID on the webpage. E.g. , ‘click [7] ’ If clicking on a specific element doesn ’ t trigger the transition to your desired web state , this is due to the element’s lack of interactivity or GUI visibility . In such cases, move on to interact with OTHER similar or relevant elements INSTEAD.
- `type [id] [content] [press enter after = 0|1]`: To type content into a field with a specific ID. By default , the ‘ Enter ’ key is pressed after typing unless ‘press enter after ’ is set to 0. E.g. , ‘type [15] [Carnegie Mellon University ] [1] ’ If you can ’ t find what you’re looking for on your first attempt , consider refining your search keywords by breaking them down or trying related terms.
- `stop [answer]`: To stop interaction and return response. Present your answer within the brackets . If the task doesn’t require a textual answer or appears insurmountable, indicate ‘N/A’ and additional reasons and all relevant information you gather as the answer . E.g. , ‘stop [5h 47min]’
- `go_home`: To return to the homepage where you can find other websites.
"""

get_action_system_prompt = """
You will be provided with the following,
OBJECTIVE:
The current subroutine you need to complete.
OBSERVATION:
A simplified text description of the current browser content, without formatting elements.
URL:
The current webpage URL
PREVIOUS ACTIONS:
A list of your past actions with an optional response
GUIDANCE TEXT:
A short text to guide you through the task-solving process.

 
You should then respond to me with :
Plan: Analyse the current situation, give the main steps to achieve it and the next action should be.
Reason: A very short explanation of what the action is doing.
Action: The action you choose to perform in the format action_name [argument_1] ... [argument_n]

Here are some general guidelines to keep in mind :
1. A subroutine is a high-level function used to perform long-range tasks. A subroutine serves as an abstraction of multiple page operations.
2. Only use a subroutine actions if needed. Page operations action are better for simple tasks.
3. You do not have access to external ressources. Limit yourself to the content of the current webpage.
4. Always refer to specific elements in the page by their ID and not by their name when using page operation actions.
5. You can't reuse the objective subroutine.

Please issue only a single action at a time.
Adhere strictly to the following output format :
RESPONSE FORMAT :
PLAN: ...
REASON: ...
ACTION: ...
"""


def get_action(objective, observation, url, previous_actions, guidance_text, relevant_policies):
    get_action_prompt = f"""
    You are an AI assistant performing tasks on a web browser.
    To solve these tasks, you will issue specific actions.

    The actions you can perform fall into two categories:

    1. Page Operation Actions:
    {page_operations}

    2. Subroutine Actions :
    {"\n".join([f"{name} [query] : {description}" for (name, description) in relevant_policies])}

    Here are some example page operations :
    {example_page_operation}

    {get_action_system_prompt}

    OBJECTIVE: {objective}
    OBSERVATION: {observation}
    URL: {url}
    PREVIOUS ACTIONS: {previous_actions}
    GUIDANCE TEXT : {guidance_text}
    """

    page_op = ["click", "type", "go_back", "go_home"]
    subroutine_actions = [name for (name, description) in relevant_policies]
    possible_actions = page_op + subroutine_actions + ["stop"]


    answer = generate_content(get_action_prompt)

    result = parse_elements(answer, ["plan", "reason", "action"])

    arguments = parse_action_call(result["action"])

    if not (arguments[0] in possible_actions):
        print(f"Impossible action : {arguments[0]}\n")

    is_page_op = arguments[0].lower() in page_op

    is_stop = arguments[0].lower() == "stop"

    action = {"name":arguments[0], "arguments":arguments[1:], "is_page_op":is_page_op,"is_stop":is_stop, "reason":result["reason"], "call":result["action"], "plan":result["plan"]}

    return action


# ==== Prompt testing ===


my_objective = """
search_nearest_place [Closest airports to the Carnegie Art Museum]
"""

my_observation = """
Tab 0 (current): OpenStreetMap\n\n[1] RootWebArea 'OpenStreetMap' focused: True\n\t[36] heading 'OpenStreetMap logo OpenStreetMap'\n\t\t[41] link 'OpenStreetMap logo OpenStreetMap'\n\t\t\t[44] img 'OpenStreetMap logo'\n\t[402] link 'Edit'\n\t[403] button ''\n\t[373] link 'History'\n\t[374] link 'Export'\n\t[407] link 'GPS Traces'\n\t[408] link 'User Diaries'\n\t[409] link 'Communities'\n\t[410] link 'Copyright'\n\t[411] link 'Help'\n\t[412] link 'About'\n\t[382] link 'Log In'\n\t[383] link 'Sign Up'\n\t[515] link 'Where is this?'\n\t[12] textbox 'Search' focused: True required: False\n\t[516] button 'Go'\n\t[503] link 'Find directions between two points'\n\t[466] heading 'Welcome to OpenStreetMap!'\n\t[469] button 'Close'\n\t[473] StaticText 'OpenStreetMap is a map of the world, created by people like you and free to use under an open license.'\n\t[474] StaticText 'Hosting is supported by '\n\t[475] link 'UCL'\n\t[477] link 'Fastly'\n\t[478] StaticText ', '\n\t[479] link 'Bytemark Hosting'\n\t[480] StaticText ', and other '\n\t[481] link 'partners'\n\t[482] StaticText '.'\n\t[485] link 'Learn More'\n\t[486] link 'Start Mapping'\n\t[23] generic 'Zoom In Zoom Out Show My Location Layers Share 50 km 50 mi \u00a9 OpenStreetMap contributors \u2665 Make a Donation. Website and API terms'\n\t\t[27] link 'Zoom In'\n\t\t[28] link 'Zoom Out'\n\t\t[30] button 'Show My Location'\n\t\t[32] link 'Layers'\n\t\t[296] link ''\n\t\t[34] link 'Share'\n\t\t[298] link ''\n\t\t[300] link ''\n\t\t[305] StaticText '50 km'\n\t\t[306] StaticText '50 mi'\n\t\t[308] StaticText '\u00a9 '\n\t\t[309] link 'OpenStreetMap contributors'\n\t\t[310] StaticText ' \u2665 '\n\t\t[311] link 'Make a Donation'\n\t\t[312] StaticText '. '\n\t\t[313] link 'Website and API terms'
"""

my_url = """
http://ec2-3-131-244-37.us-east-2.compute.amazonaws.com:3000/#map=7/42.896/-75.108
"""

my_previous_actions = """
"""

my_guidance_text = """
Please follow these instructions to solve the subtask:
1. For searches that refer to CMU, e.g.  "find cafes near CMU Hunt Library"
a. You have to first center your map around a location. If you have to find cafes near CMU Hunt Library, the first step is to make sure the map is centered around Carnegie Mellon University. To do that, first search for Carnegie Mellon University and then click [] on a list of location that appears. You MUST click on the Carnegie Mellon University location to center the map. Else the map will not centered. E.g click [646]
b. Now that your map is centered around Carnegie Mellon University, directly search for "cafes near Hunt Library". Do not include the word CMU in the search item.
The word CMU cannot be parsed by maps and will result in an invalid search.
c. When your search returns a list of elements, return them in a structured format like stop [A, B, C]
2. For searches that don't refer to CMU
a. No need to center the map. Directly search what is specified in OBJECTIVE, e.g. "bars near Carnegie Music Hall"
b. When your search returns a list of elements, return them in a structured format like stop [A, B, C]
3. Be sure to double check whether the OBJECTIVE has CMU or not and then choose between instruction 1 and 2. 
4. Remember that the word CMU cannot be typed in the search bar as it cannot be parsed by maps. 
5. Remember that if you want to center your map around Carnegie Mellon University, you have to click on it after you search for it. Check your PREVIOUS ACTIONS to confirm you have done so, e.g. click [646] should be in the previous actions.
"""

my_relevant_policies = [
("find_directions", "This Maps subroutine finds directions between two locations to answer the query.")
]


def get_my_action():
    return get_action(my_objective, my_observation, my_url, my_previous_actions, my_guidance_text, my_relevant_policies)