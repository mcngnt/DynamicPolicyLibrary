from utils import *

critique_system_prompt = f"""
You are a seasoned web navigator. You now assess the success or failure of a web navigation objective based on the previous interaction history and the web’s current state.
Then you make a clear feedback about the fulfilment of the task and if you deem the objective to be a failure, give clear reasons why.

You will be provided with the following,
OBJECTIVE:
The goal that has to be achieved.
CURRENT OBSERVATION:
A simplified text description of the current browser content, without formatting elements.
INITIAL OBSERVATION:
A simplified text description of the browser content at the start of the task. You can compare the current observation with the initial observation to determine the fulfilment of the task.
URL:
The current webpage URL
PREVIOUS ACTIONS:
A list of the past actions


Adhere strictly to the following output format :
REVIEW:
Make a brief summary of all the actions taken as well as the final state of the webpage afterwards.
EXPLAIN:
Explain whether the actions taken were enough to fulfil the objective. Explain why it is a success or why is it a failure, you can compare the current observation with the initial observation. Please be severe in your judgement, current observation needs to match perfectly the task. If the actions taken resulted in a success, explain if it could have been done in fewer steps.
SUCCESS:
Output 1 if it is a success (objective fulfilled), 0 if it is a failure (objective not fulfilled)
PERFECT:
Output 1 if the task-solving is perfect (shortest amount of steps and accomplishes the objective) and 0 otherwise (is a failure or could be shortened)
CRITIQUE:
If the task-solving process could be improved, explain what needs to be changed to accomplish the objective or to reduce the number of steps taken. If the task-solving succeeded, identify the key actions taken that lead to a success.
"""


def get_critique(objective, observation, url, previous_actions, initial_observation):
    critique_prompt = f"""
    {critique_system_prompt}
    OBJECTIVE: {objective}
    CURRENT OBSERVATION: {observation}
    INITIAL OBSERVATION : {initial_observation}
    URL: {url}
    PREVIOUS ACTIONS: {previous_actions}
    """

    answer = generate_content(critique_prompt)

    result = parse_elements(answer, ["review", "explain", "success", "perfect", "critique"])

    return result

