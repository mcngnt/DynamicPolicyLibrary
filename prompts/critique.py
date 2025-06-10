from utils import *

critique_system_prompt = f"""
You are a seasoned web navigator. You now assess the success or failure of a web navigation objective based on the previous interaction history and the web’s current state.
Then you make a clear feedback about the fulfilment of the task, giving the reasons of success of failures and possible new trajectories to explore.

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
A list of the past actions, along with their intents during navigation. Be aware that it is only an intent and not always what really happened.


Here is the expected output:

EXPLAIN:
Make a brief summary of the current observation state and the initial observation state. Then, by comparing the current observation with the initial observation, explain why is the task a success or a failure related to the objective. Please be severe in your judgement, current observation needs to perfectly achieve the task.
SUCCESS:
Output 1 if it is a success (objective fulfilled), 0 if it is a failure (objective not fulfilled) (output only an int)
BREAKDOWN:
Make a long and detailed summary of all the actions taken as an ordered list with redundant actions removed and no page ID mentionned.
FEEDBACK:
Based on SUCCESS, explain if the task is a success or a failure and why it is a success or a failure. 
If it is a success : Describe the key actions that have to be taken to be able to reproduce the same navigation outcome as an ordered list. The key actions need to be precise and given chronologically. Be aware that if two actions seem to achieve the same thing in the breakdown, the latter is probably a key action and the former a mistake.
If it is a failure : Suggest a new plan as an ordered list that the agent could try instead of the current trajectory to solve the task.


Here is an example:

EXPLAIN:
The INITIAL OBSERVATION showed a dashboard listing 24 issues across various projects, with no explicit "urgent" filter or sorting applied. The CURRENT OBSERVATION displays the `mcngnt-card-project` project’s issues page with the URL `?sort=title_dsc&state=opened&label_name%5B%5D=urgent`, indicating successful filtering for "urgent" labels and sorting by title in descending order. Two matching issues ("Color theme slider" and "WCAG trash panda mode") are listed, confirming the filter. The sort order is explicitly set to "descending" via the `Sort direction` button.
SUCCESS:  
1
BREAKDOWN:  
1. Navigate to the `mcngnt-card-project` project issues page.  
2. Apply the "urgent" label filter (e.g., via link or textbox).  
3. Select "Title" as the sort criteria.  
4. Ensure sorting direction is set to "Descending".  
FEEDBACK: 
The task is a success because the current page filters issues by "urgent" and sorts them by title in descending order, perfectly matching the objective.  

Key Actions to Reproduce: 
1. Filter issues by the "urgent" label (e.g., click the "urgent" link in labels or type in the filter textbox).  
2. Click the "Title" sort button.  
3. Verify the sort direction is "Descending" (adjust if necessary).  

Notes on Previous Actions: 
- Redundant clicks on non-functional sort menus (e.g., "Priority") were errors but did not derail the outcome.  
- The critical step was successfully applying the "urgent" filter and title-based sorting.


Adhere strictly to the following YAML output format (CATEGORY in capital letters followed directly by a colon) :
EXPLAIN:
Brief summary and explanation
SUCCESS:
1 or 0
BREAKDOWN:
Detailed list summary
FEEDBACK:
Key actions or new plan
"""

# Do not include breakdown if failure
# actually differentiate success and failure


def get_critique(objective, observation, url, previous_actions, initial_observation):
    critique_prompt = f"""
    {critique_system_prompt}
    OBJECTIVE:
    {objective}
    CURRENT OBSERVATION:
    {observation}
    INITIAL OBSERVATION :
    {initial_observation}
    URL:
    {url}
    PREVIOUS ACTIONS:
    {previous_actions}
    """

    # print(critique_prompt)

    # print(len(previous_actions))

    answer = generate_content(critique_prompt)

    # print(answer)

    # return answer 
    result = parse_elements(answer, ["explain", "success", "breakdown", "feedback"])

    return result



# describe how to achieve the task in general


# Describe the key actions that have to be taken to be able to reproduce the same navigation outcome as an ordered list. The key actions need to be very precise and given chronologically. In case of failure, you can also suggest a new sequence of actions thta the agent could try to solve the task.

# The later actions performed are probably the most important and you should spend more time detailing them.