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


At each round of conversation, I will give you
 Task name : ...
 Task description : ...
 Query with which the task was performed : ...
 All the actions and observations from the last round : ...
 Critique of the previous interactions : ...
 Guidance text from the last round : ...


 You should then respond to me with
 Explain (if applicable): What are the exact causes of failure and how to solve them ? Why is the guidance not enough to complete the task? What does the critique answer implies ?
 Plan: How to complete the task step by step. Do not be too specific, your guidance text should be able to handle multiple queries.
 Guidance text :
 1) Write a guidance text to be used by a web agent to complete a specific tesk.
 2) Don't be too specific, your guidance text should generalize to multiple queries
 3) Write the guidance text for the general task, not for the query associated with the task
 4) Keep all the information in the previous guidance text. Only remove information from the previous guidance text if you think it is useless or nocive.
 5) Do not mention any specific query in the guidance text. The guidance text should be applicable to a large range of queries
 6) Do not make too drastic changes to the original guidance text. The improvement process should be gradual.
 7) Be precise. Do not be afraid to give too many details.

 RESPONSE FORMAT:
 EXPLAIN: ...
 PLAN:
 1) ...
 2) ...
 3) ...
 GUIDANCE: ...
"""

# def extract_guidance(text):
#     match = re.search(r"'''(.*?)'''", text, re.DOTALL)
#     return match.group(1) if match else None


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

    result["guidance"] += "\nPlease, use ONLY page operation and no subroutine actions."

    return result
