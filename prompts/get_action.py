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
DESCRIPTION:
The description of the subroutine you have to complete.
OBSERVATION:
A simplified text description of the current browser content, without formatting elements.
URL:
The current webpage URL
PREVIOUS ACTIONS:
A list of your past actions along with a quick description of what they were supposed to do.
GUIDANCE TEXT:
A short text to guide you through the task-solving process.

 
You should then respond to me with :
Plan: Analyse the current situation, give the main steps to achieve it and the next action should be.
Reason: A very short explanation of what the action is doing.
Action: The action you choose to perform in the format action_name [argument_1] ... [argument_n]

Here are some general guidelines to keep in mind :
1. A subroutine is a high-level function used to perform long-range tasks. A subroutine serves as an abstraction of multiple page operations.
2. Only use a subroutine actions if needed. Page operations action are better for simple tasks.
3. You do not have access to external resources. Limit yourself to the content of the current webpage.
4. Always refer to specific elements in the page by their ID and not by their name when using page operation actions.
5. You can't reuse the objective subroutine.

Please issue only a single action at a time.
Adhere strictly to the following output format :
RESPONSE FORMAT :
PLAN: ...
REASON: ...
ACTION: ...
"""


def get_action(objective, description, observation, url, previous_actions, guidance_text, relevant_policies):
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
    DESCRIPTION: {description}
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
