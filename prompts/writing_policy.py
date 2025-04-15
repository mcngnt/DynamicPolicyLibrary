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
* Once you have navigated to any specific subreddit, return stop [N/A]. Even if the subreddit is generally related and not specific to your quwey, stop here and do not try to search again for another subreddit."
"


You will be provided with the following,
TASK NAME:
The name of the task the agent had to solve.
TASK DESCRIPTION:
A textual description of the goal of the task.
QUERY:
The specific objective to which the task was applied.
PREVIOUS ACTIONS:
A list of your past actions along with a quick description of what they were supposed to do.
CRITIQUE:
A textual criticism of the previous actions to assess the fulfilment of the task.
OLD GUIDANCE:
Guidance text from the previous iteration.


You should then respond to me with:
Explain: Highlight the main actions performed to try solving the tasks. Please refer to the critique to answer the following questions : If the task was fulfilled, what key actions were done to achieve it ? If the task was not fulfilled, what actions could have been done based on the current observation ? Are there any unnecessary steps ?
Plan: Based on the explanation, provide a step-by-step plan of how to solve the task. If the previous actions lead to a failure, try to be creative and invent a new path to not make the same mistakes.
Guidance: Based on your plan and explanation, write general directions for the web agent to solve the task. Your guidance should be ordered as bullet points and only include the key actions highlighted in your plan and explanation.

Here are some general guidelines to keep in mind for the guidance text:
 1) Write a guidance text to be used by a web agent to achieve a specific task.
 2) Don't be too specific, your guidance text should generalize to multiple queries
 3) Do not mention any specific query in the guidance text. The guidance text should be applicable to a wide range of queries
 4) Only give information about the tricky steps of the task-solving process. The agent is capable and independent for simple actions.
 5) Change the granularity of your guidance depending on the importance of the action. The more important an action is, the more detailed it needs to be.

 RESPONSE FORMAT:
 EXPLAIN: ...
 PLAN: ...
 GUIDANCE: ...
"""



def write_policy(task_name, task_description, arguments, observation, critique, previous_guidance):
    writing_prompt = f"""
    {writing_system_prompt}
    Task name : {task_name}
    Task description : "{task_description}"
    Query with which the task was performed : {arguments}
    Example website on which the task could be completed : {observation}
    Critique : {critique}
    Guidance text from the last round : {previous_guidance}
    """

    answer = generate_content(writing_prompt)

    # Return only generated policy from answer

    result = parse_elements(answer, ["explain", "plan", "guidance"])

    return result
