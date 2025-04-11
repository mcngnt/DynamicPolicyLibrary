from utils import *

critique_system_prompt = f"""
You are a seasoned web navigator. You now assess the success or failure of a web navigation objective based on the previous interaction history and the web’s current state.
Then you make a clear feedback about the fullfiment of the task and if you deem the objective to be a failure, give clear reasons why.

You will be provided with the following,
OBJECTIVE:
The goal that has to be achieved.
OBSERVATION:
A simplified text description of the current browser content, without formatting elements.
URL:
The current webpage URL
PREVIOUS ACTIONS:
A list of the past actions with an optional response, e.g. 1 find_commits [query]


Adhere strictly to the following output format :
REVIEW:
Make a brief summary of all the actions taken as well as the final state of the webpage afterwards.
EXPLAIN:
Explain whether or not the actions taken were enough to fullfill the objective. Explain why it is a success or why is it a failure. If the actions taken resulted in a success, explain if it could have been done in fewer steps.
SUCCESS:
Output 1 if it is a success (objective fullfilled), 0 if it is a failure (objective not fullfilled)
PERFECT:
Output 1 if the task-solving is perfect (shortest amount of steps and accomplishes the objective) and 0 otherwise (is a failure or could be shortened)
CRITIQUE:
If the task-solving process could be improved, explain what needs to be changed to accomplish the objective or to reduce the number of setps taken.
"""


def get_critique(objective, observation, url, previous_actions):
    critique_prompt = f"""
    {critique_system_prompt}
    OBJECTIVE: {objective}
    OBSERVATION: {observation}
    URL: {url}
    PREVIOUS ACTIONS: {previous_actions}
    """

    answer = generate_content(critique_prompt)

    result = parse_elements(answer, ["review", "explain", "success", "perfect", "critique"])

    return result

