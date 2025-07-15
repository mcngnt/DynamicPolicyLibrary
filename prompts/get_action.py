from utils import *



example_page_operation = """
click [7]
type [15] [Carnegie Melon University] [1]
go_home
stop [Closed]
note [Spent $10 on 4/1/2024]
stop [N/A]
type [789] [Best selling books] [0]
go_back
"""

example_subroutines = """
find_directions [Check if the social security administration in pittsburgh can be reached in one hour by car from Carnegie Mellon University]
search_nearest_place [Tell me the closest cafe(s) to CMU Hunt library]
list_products [List products from PS4 accessories category by ascending price]
search_reviews [List out reviewers, if exist, who mention about ear cups being small]
create_project [Create a new public project "awesome-llms" and add primer, convexegg, abishek as members]
create_group [Create a new group "coding_friends" with members qhduan, Agnes-U]
find_subreddit [most appropriate subreddit for X]
find_user [AdamCannon]
find_customer_review [Show me customer reviews for Zoe products]
find_order [Most recent pending order by Sarah Miller]
"""

page_operations = """

- `click [id]`: To click on an element with its numerical ID on the webpage. E.g. , ‘click [7] ’ If clicking on a specific element doesn ’ t trigger the transition to your desired web state , this is due to the element’s lack of interactivity or GUI visibility . In such cases, move on to interact with OTHER similar or relevant elements INSTEAD.
- `type [id] [content] [press enter after = 0|1]`: To type content into a field with a specific ID. By default , the ‘ Enter ’ key is pressed after typing unless ‘press enter after ’ is set to 0. E.g. , ‘type [15] [Carnegie Mellon University ] [1] ’ If you can ’ t find what you’re looking for on your first attempt , consider refining your search keywords by breaking them down or trying related terms.
- `go_home`: To return to the homepage.
- `go_back`: Revert to the previous state of the page.
"""

get_action_system_prompt = """
You will be provided with the following,
OBJECTIVE:
The current objective you need to complete.
PLAN:
The plan to solve the objective. Try to follow it and use PREVIOUS ACTIONS to determine its progression.
DESCRIPTION:
The description of the type of objective you need to complete (empty if the objective is self-explanatory)
OBSERVATION:
A simplified text description of the current browser content, without formatting elements.
URL:
The current webpage URL
PREVIOUS ACTIONS:
A list of the past actions, along with their intents during navigation. Be aware that it is only an intent and not always what really happened.
GUIDANCE TEXT:
A short text to guide you through the task-solving process. Follow it closely.


Here are some general guidelines to keep in mind :
- A subroutine is a high-level function used to perform long-range tasks. A subroutine serves as an abstraction of multiple page operations.
- You do not have access to external resources. Limit yourself to the content of the current webpage.
- Always refer to specific elements in the page by their ID and not by their name when using page operation actions.
- You can't reuse the objective subroutine.
- If what you want to do fails, use stop [N/A] instead of endlessly repeating the same sequence of actions (you can spot such a sequence by looking at PREVIOUS ACTIONS)
- Do not try to directly change the url to accomplish the goal. Use the interface instead of guessing the right url by using the searchbar for instance.

Please issue only a single action at a time.
Adhere strictly to the following YAML output format (CATEGORY in capital letters followed directly by a colon) :
EXPLANATION:
Based on all the provided information, explain what action you should take to progress towards the objective.
ACTION:
action_name [argument_1] ... [argument_n]
REASON:
A very short text (20 words max) describing the purpose of your action
"""


def get_action(objective, description, observation, url, previous_actions, guidance_text, relevant_policies, is_root, plan="", step_nb=0):
    subroutine_actions_prompt = "\n".join([f"{name} [query] : {description}" for (name, description) in relevant_policies])

    plan = "" if len(plan)==0 else "\n" + plan
    # is_root = is_root and step_nb == 0

    get_action_prompt = f"""
    You are an AI assistant performing actions to solve tasks on a web browser.

    The actions you can perform fall into several categories:

    {"- Page Operation Actions:" + page_operations if not is_root else ""}

    - Subroutine Actions:
    {subroutine_actions_prompt}

    - Stop Action:
    `stop [answer]`: To stop interaction and return response. Present your answer within the brackets . If the task doesn’t require a textual answer or appears insurmountable, indicate ‘N/A’ and additional reasons and all relevant information you gather as the answer . E.g. , ‘stop [5h 47min]’

    Here are some example actions:
    {example_page_operation if not is_root else ""}
    {example_subroutines}

    {get_action_system_prompt}

    OBJECTIVE:
    {objective}
    {"" if len(plan)=="" or not is_root else "PLAN:"+plan}
    DESCRIPTON:
    {description}
    OBSERVATION:
    {observation}
    URL:
    {url}
    PREVIOUS ACTIONS:
    {previous_actions}
    GUIDANCE TEXT :
    {guidance_text}
    """

    page_op = ["click", "type", "go_back", "go_home", "scroll"]
    subroutine_actions = [name for (name, description) in relevant_policies]
    possible_actions = page_op + subroutine_actions + ["stop"]


    answer = generate_content(get_action_prompt)


    try:
        result = parse_elements(answer, ["reason", "action"])

        arguments = parse_action_call(result["action"])

        if not (arguments[0] in possible_actions):
            raise Exception(f"Impossible action : {arguments[0]}\n")

        is_page_op = arguments[0].lower() in page_op

        is_stop = arguments[0].lower() == "stop"

        action = {"name":arguments[0], "arguments":arguments[1:], "is_page_op":is_page_op,"is_stop":is_stop, "reason":result["reason"], "call":result["action"]}

        return action
    except:
        return get_action(objective, description, observation, url, previous_actions, guidance_text, relevant_policies, is_root, plan)
