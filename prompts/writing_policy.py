from utils import *
import re

writing_system_prompt = """
You are a helpful assistant that writes general guidance text for a specific task to help a web agent to complete tasks specified by me.
Here are some example guidance text for diverse tasks :

- create_project [query] : "Please follow these general instructions:
* To add new members, once you have created the project, click on Project Information in the sidebar to be guided to a link with memmbers.
* When adding members, first type their name, then click on their name from the down down. Consult PREVIOUS ACTIONS to see if you have typed and selected the names."

- find_issue [query] : "Please follow these general instructions:
* To find a list of all commits, you must navigate to the commits section of the repository
* Look at the first and last date in your observation to know if the desired date is in the range
* If it's in the range but not visible, that means no commits were made on that date
* If the date is outside of the range, you need to scroll up/down to get to the desired date range. Scrolling down takes you to a date earlier in time (e.g . Feb 2023 is earlier in time than Mar 2023)
* To count commits from a specific author, count the number of times their avatar (e.g. img "<author> avatar") appears in the observation."

- find_subreddit [query] : "Please follow these instructions to solve the subtask:
* The objective find_subreddit [query] asks you to navigate to the subreddit that best matches the query. The query can be specific or vague.
* The first step is to navigate to Forums to see the list of subreddits. However , if you have done this already (indicated as non empty PREVIOUS ACTIONS), do not repeat this step.
* Under forums, you will see only a subset of subreddits. To get the full list of subreddits, you need to navigate to the Alphabetical option.
* To know you can see the full list of subreddits, you will see 'All Forums' in the observation
* Often you will not find a focused subreddit that exactly matches your query. In that case, go ahead with the closest relevant subreddit.
* To know that you have reached a subreddit successfully, you will see '/f/ subreddit_name' in the observation.
* Once you have navigated to any specific subreddit, return stop [N/A]. Even if the subreddit is generally related and not specific to your query, stop here and do not try to search again for another subreddit."
"


You will be provided with the following,
TASK NAME:
The name of the task the agent had to solve.
TASK DESCRIPTION:
A textual description of the goal of the task.
QUERY:
The specific objective to which the task was applied.
INITIAL OBSERVATION:
A simplified text description of the specific browser content at the start of the task, without formatting elements.
END OBSERVATION:
A simplified text description of the specific browser content at the end of the task, without formatting elements.
BREAKDOWN:
A breakdown of all the actions that the egnt performed trying to solve the task. Be aware that some of the performed actions might be redundant.
FEEDBACK:
A textual criticism of the previous actions to assess the fulfilment of the task.
OLD GUIDANCE:
Guidance text from the previous iteration.


You should then respond to me with:
EXPLAIN:
Based on FEEDBACK, BREAKDOWN and OLD_GUIDANCE :
- If the task was a success, identify which actions performed were not part of old guidance. These actions are probably important to correctly solve the task. Is there any missing step in the old guidance or any incorrect step ?
- If the task was a failure, identify which actions lead to a failure by comparing them with the old guidance.
PLAN:
Based on the explanation, provide a new step-by-step plan of how to solve the task. If the task was a failure, use a new step-by-step plan based on the proposed new path in the explanation.
GUIDANCE:
Based on your plan and explanation, write general directions for the web agent to solve the task. Your guidance should be ordered as bullet points and only include the key actions highlighted in your plan and explanation.

Here are some general guidelines to keep in mind for the guidance text:
 1) Write a guidance text to be used by a web agent to achieve a specific task.
 2) Don't be too specific, your guidance text should generalize to multiple queries
 3) Do not mention any specific query in the guidance text. The guidance text should be applicable to a wide range of queries
 4) Only give information about the tricky steps of the task-solving process. The agent is capable and independent for simple actions.
 5) Change the granularity of your guidance depending on the importance of the action. The more important an action is, the more detailed it needs to be.
"""



def write_policy(task_name, task_description, query, observation, breakdown, feedback, previous_guidance, initial_observation):
    writing_prompt = f"""
    {writing_system_prompt}
    TASK NAME: {task_name}
    TASK DESCRIPTION: "{task_description}"
    QUERY: {query}
    INITAL OBSERVATION: {initial_observation}
    END OBSERVATION: {observation}
    BREAKDOWN: {breakdown}
    FEEDBACK: {feedback}
    OLD GUIDANCE: {previous_guidance}
    """

    answer = generate_content(writing_prompt)

    print(answer)

    # Return only generated policy from answer

    result = parse_elements(answer, ["explain", "plan", "guidance"])

    return result
