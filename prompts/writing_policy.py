from utils import *
import re

# writing_system_prompt = """
# You are a helpful assistant that writes general guidance text for a specific task to help a web agent to complete tasks specified by me.
# Here are some example guidance text for diverse tasks :

# - create_project [query] : "Please follow these general instructions:
# * To add new members, once you have created the project, click on Project Information in the sidebar to be guided to a link with memmbers.
# * When adding members, first type their name, then click on their name from the down down. Consult PREVIOUS ACTIONS to see if you have typed and selected the names."

# - find_commits [query] : "* To find a list of all commits, you must navigate to the commits section of the repository\n* Look at the first and last date in your observation to know if the desired date is in the range\n* If it's in the range but not visible, that means no commits were made on that date\n* If the date is outside of the range, you need to scroll up/down to get to the desired date range. Scrolling down takes you to a date earlier in time (e.g. Feb 2023 is earlier in time than Mar 2023)\n* To count commits from a specific author, count the number of times their avatar (e.g. img \"<author> avatar\") appears in the observation\n\nHere are a few examples:\n### Input:\n \nOBJECTIVE:\nfind_commits [How many commits did Mike Perotti make to diffusionProject on 02/02/2023?]\nOBSERVATION:\n[8420] StaticText '02 Feb, 2023'\n    [8423] StaticText '3 commits'\n    [8426] img \"Mike Perrotti's avatar\"\n    [8428] link 'Coverage improvements (#449)'\n    [8433] link 'Mike Perrotti'\n    [8434] StaticText ' authored '\n    [8435] time 'Feb 1, 2023 10:43pm EST'\n        [8437] StaticText '1 year ago'\n    [10354] button 'Unverified'\n    [8444] StaticText 'a323cbb6'\n    [8442] button 'Copy commit SHA' live: polite atomic: False relevant: additions text\n    [8443] link 'Browse Files'\n    [8455] img \"Mike Perrotti's avatar\"\n    [8457] link 'updates guidance about numeric table values to be more specific (#451)\n    [8462] link 'Mike Perrotti'\n    [8463] StaticText ' authored '\n    [8464] time 'Feb 1, 2023 10:26pm EST'\n        [8466] StaticText '1 year ago'\n    [10356] button 'Unverified'\n    [8473] StaticText '9bf4ae35'\n    [8471] button 'Copy commit SHA' live: polite atomic: False relevant: additions text\n    [8472] link 'Browse Files'\n    [8484] img \"Emily Brick's avatar\"\n    [8486] link 'Correct typos on Contributing Guidelines and Follow (#1518)'\n    [8491] link 'Emily Brick'\n    [8492] StaticText ' authored '\n    [8493] time 'Feb 1, 2023 7:40pm EST'\n        [8495] StaticText '1 year ago'\nURL:\nhttps://webarena-env-github.awsdev.asapp.com/\nPREVIOUS ACTIONS:\nclick [3373]\nscroll [down]\nscroll [down]\n\n\n### Response:\n\nREASON:\nThe objective is to find how many commits Mike Perotti made on Feb 2, 2023. I see that there has been 3 commits on 02 Feb, 2023.\nHowever, I must count number of times img \"Mike Perrotti's avatar\" appears. \nI see [8426] img \"Mike Perrotti's avatar\", [8455] img \"Mike Perrotti's avatar\". \nCounting this leads to 2 commits made by Mike Perotti. In summary, the next action I will perform is ```stop [2]```\nACTION:\nstop [2]"

# - find_subreddit [query] : "Please follow these instructions to solve the subtask:
# * The objective find_subreddit [query] asks you to navigate to the subreddit that best matches the query. The query can be specific or vague.
# * The first step is to navigate to Forums to see the list of subreddits. However , if you have done this already (indicated as non empty PREVIOUS ACTIONS), do not repeat this step.
# * Under forums, you will see only a subset of subreddits. To get the full list of subreddits, you need to navigate to the Alphabetical option.
# * To know you can see the full list of subreddits, you will see 'All Forums' in the observation
# * Often you will not find a focused subreddit that exactly matches your query. In that case, go ahead with the closest relevant subreddit.
# * To know that you have reached a subreddit successfully, you will see '/f/ subreddit_name' in the observation.
# * Once you have navigated to any specific subreddit, return stop [N/A]. Even if the subreddit is generally related and not specific to your query, stop here and do not try to search again for another subreddit."
# "

writing_system_prompt = """
You are a helpful assistant that writes general guidance text for a specific task to help a web agent to complete tasks specified by me.
Here are some example guidance text for diverse tasks :

 - find_commits [query] : "* To find a list of all commits, you must navigate to the commits section of the repository\n* Look at the first and last date in your observation to know if the desired date is in the range\n* If it's in the range but not visible, that means no commits were made on that date\n* If the date is outside of the range, you need to scroll up/down to get to the desired date range. Scrolling down takes you to a date earlier in time (e.g. Feb 2023 is earlier in time than Mar 2023)\n* To count commits from a specific author, count the number of times their avatar (e.g. img \"<author> avatar\") appears in the observation\n\nHere are a few examples:\n### Input:\n \nOBJECTIVE:\nfind_commits [How many commits did Mike Perotti make to diffusionProject on 02/02/2023?]\nOBSERVATION:\n[8420] StaticText '02 Feb, 2023'\n    [8423] StaticText '3 commits'\n    [8426] img \"Mike Perrotti's avatar\"\n    [8428] link 'Coverage improvements (#449)'\n    [8433] link 'Mike Perrotti'\n    [8434] StaticText ' authored '\n    [8435] time 'Feb 1, 2023 10:43pm EST'\n        [8437] StaticText '1 year ago'\n    [10354] button 'Unverified'\n    [8444] StaticText 'a323cbb6'\n    [8442] button 'Copy commit SHA' live: polite atomic: False relevant: additions text\n    [8443] link 'Browse Files'\n    [8455] img \"Mike Perrotti's avatar\"\n    [8457] link 'updates guidance about numeric table values to be more specific (#451)\n    [8462] link 'Mike Perrotti'\n    [8463] StaticText ' authored '\n    [8464] time 'Feb 1, 2023 10:26pm EST'\n        [8466] StaticText '1 year ago'\n    [10356] button 'Unverified'\n    [8473] StaticText '9bf4ae35'\n    [8471] button 'Copy commit SHA' live: polite atomic: False relevant: additions text\n    [8472] link 'Browse Files'\n    [8484] img \"Emily Brick's avatar\"\n    [8486] link 'Correct typos on Contributing Guidelines and Follow (#1518)'\n    [8491] link 'Emily Brick'\n    [8492] StaticText ' authored '\n    [8493] time 'Feb 1, 2023 7:40pm EST'\n        [8495] StaticText '1 year ago'\nURL:\nhttps://webarena-env-github.awsdev.asapp.com/\nPREVIOUS ACTIONS:\nclick [3373]\nscroll [down]\nscroll [down]\n\n\n### Response:\n\nREASON:\nThe objective is to find how many commits Mike Perotti made on Feb 2, 2023. I see that there has been 3 commits on 02 Feb, 2023.\nHowever, I must count number of times img \"Mike Perrotti's avatar\" appears. \nI see [8426] img \"Mike Perrotti's avatar\", [8455] img \"Mike Perrotti's avatar\". \nCounting this leads to 2 commits made by Mike Perotti. In summary, the next action I will perform is ```stop [2]```\nACTION:\nstop [2]"

- find_subreddit [query] : "Please follow these instructions to solve the subtask:
 * The objective find_subreddit [query] asks you to navigate to the subreddit that best matches the query. The query can be specific or vague.
 * The first step is to navigate to Forums to see the list of subreddits. However , if you have done this already (indicated as non empty PREVIOUS ACTIONS), do not repeat this step.
 * Under forums, you will see only a subset of subreddits. To get the full list of subreddits, you need to navigate to the Alphabetical option.
 * To know you can see the full list of subreddits, you will see 'All Forums' in the observation
 * Often you will not find a focused subreddit that exactly matches your query. In that case, go ahead with the closest relevant subreddit.
 * To know that you have reached a subreddit successfully, you will see '/f/ subreddit_name' in the observation.
 * Once you have navigated to any specific subreddit, return stop [N/A]. Even if the subreddit is generally related and not specific to your query, stop here and do not try to search again for another subreddit."

- find_customer_review [query] : "* The objective find_customer_review [query] asks you to navigate to the product page containing customer reviews. \n* To navigate to a review, first click on REPORTS in the side panel\n* Once you have clicked on REPORTS, and you see the Reports panel with Marketing, Sales, Reviews, Customers etc, click on By Products under Customers.\n* Once you are in the Product Reviews Report, you need to locate the product by searching for it. Use the gridcell below Product to search for a product. Do not use other search boxes. Look at the example below where I show you how to search for Zoe in the correct gridcell. \n* When searching for a product, search the first word only like Zoe, or Antonia or Chloe. \n* Once the product shows up, click on 'Show Reviews'.\n7. Once all the reviews show up, return stop [N/A] to hand back control to the agent that queried you.\n\nHere are a few examples:\n### Input:\n\nOBJECTIVE:\nfind_product_review [Show me the review of the customer who is the most unhappy with the style of Zoe products]\nOBSERVATION:\nTab 0 (current): Product Reviews Report / Reviews / Reports / Magento Admin\n\t\t[1992] table ''\n\t\t\t[2723] row ''\n\t\t\t\t[2724] columnheader 'ID' required: False\n\t\t\t\t[2725] columnheader 'Product' required: False\n\t\t\t\t[2726] columnheader '\u2191 Reviews' required: False\n\t\t\t\t[2727] columnheader 'Average' required: False\n\t\t\t\t[2728] columnheader 'Average (Approved)' required: False\n\t\t\t\t[2729] columnheader 'Last Review' required: False\n\t\t\t\t[2730] columnheader 'Action' required: False\n\t\t\t[1994] row ''\n\t\t\t\t[1995] gridcell '' required: False\n\t\t\t\t\t[1996] textbox '' required: False\n\t\t\t\t[1997] gridcell '' required: False\n\t\t\t\t\t[1998] textbox '' required: False\n\t\t\t\t[1999] gridcell '' required: False\n\t\t\t\t\t[2000] textbox '' required: False\n\t\t\t\t[2001] gridcell '' required: False\n\t\t\t\t\t[2002] textbox '' required: False\n\t\t\t\t[2003] gridcell '' required: False\n\t\t\t\t\t[2004] textbox '' required: False\n\t\t\t\t[2005] gridcell 'undefined \\ue627 undefined \\ue627' required: False\n\t\t\t\t\t[2008] textbox 'From' required: False\n\t\t\t\t\t[3196] button 'undefined \\ue627'\n\t\t\t\t\t[2010] textbox 'To' required: False\n\t\t\t\t\t[3201] button 'undefined \\ue627'\n\t\t\t\t[2747] gridcell '\\xa0' required: False\n\t\t\t[2759] row 'https://webarena-env-cms.awsdev.asapp.com/admin/review/product/index/productId/1620/'\n\t\t\t\t[2779] gridcell '1620' required: False\n\t\t\t\t[2780] gridcell 'Erica Evercool Sports Bra' required: False\n\t\t\t\t[2781] gridcell '4' required: False\n\t\t\t\t[2782] gridcell '60.0000' required: False\n\t\t\t\t[2783] gridcell '60.0000' required: False\n\t\t\t\t[2784] gridcell 'Apr 19, 2023, 12:15:19 PM' required: False\n\t\t\t\t[2785] gridcell 'Show Reviews' required: False\n\t\t\t\t\t[2792] link 'Show Reviews'\n\t\t\t[2760] row 'https://webarena-env-cms.awsdev.asapp.com/admin/review/product/index/productId/39/'\n\t\t\t\t[2794] gridcell '39' required: False\n\t\t\t\t[2795] gridcell \nURL:\nhttps://webarena-env-cms.awsdev.asapp.com/admin/reports/report_review/product/\nPREVIOUS ACTIONS:\nclick [1195]\nclick [1531]\n\n\n### Response:\n\nREASON:\nLet's think step-by-step. We are in the Product Review Report page. We have to search for a Zoe product. To do so, I have to type in Zoe in a gridcell corresponding to the Product column. The Product column is the second column after ID. Therefore I have to find the second gridcell just below it. The first one is 1995, and the second one is 1997.  In summary, the next action I will perform is type [1997] [Zoe] [1]\nACTION:\ntype [1997] [Zoe] [1]"



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

Here are some general guidelines to keep in mind for the guidance text:
- Write a guidance text to be used by a web agent to achieve a specific task.
- Don't be too specific, your guidance text should generalize to multiple queries
- Do not mention any specific query in the guidance text, except in the examples. The guidance text should be applicable to a wide range of queries
- Only give information about the tricky steps of the task-solving process. The agent is capable and independent for simple actions.
- Change the granularity of your guidance depending on the importance of the action. The more important an action is, the more detailed it needs to be.
- Try to include examples of how to use the policy at the end of the guidance text. You can use INITIAL OBSERVATION and END OBSERVATION as inspiration.

Adhere strictly to the following YAML output format :
EXPLAIN:
Based on FEEDBACK, BREAKDOWN and OLD_GUIDANCE :
- If the task was a success, identify which actions performed were not part of old guidance. These actions are probably important to correctly solve the task. Is there any missing step in the old guidance or any incorrect step ?
- If the task was a failure, identify which actions lead to a failure by comparing them with the old guidance.
PLAN:
Based on the explanation, provide a new step-by-step plan of how to solve the task. If the task was a failure, use a new step-by-step plan based on the proposed new path in the explanation.
GUIDANCE:
Based on your plan and explanation, write general directions for the web agent to solve the task as well as examples. Your guidance should be ordered as bullet points and only include the key actions highlighted in your plan and explanation.
"""



def write_policy(task_name, task_description, query, observation, breakdown, feedback, previous_guidance, initial_observation):
    writing_prompt = f"""
    {writing_system_prompt}
    TASK NAME:
    {task_name}
    TASK DESCRIPTION:
    {task_description}
    QUERY:
    {query}
    INITAL OBSERVATION:
    {initial_observation}
    END OBSERVATION:
    {observation}
    BREAKDOWN:
    {breakdown}
    FEEDBACK:
    {feedback}
    OLD GUIDANCE:
    {previous_guidance}
    """

    answer = generate_content(writing_prompt)

    # print(answer)

    # Return only generated policy from answer

    result = parse_elements(answer, ["explain", "plan", "guidance"])

    return result
