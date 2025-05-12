from utils import *
import json

github_agent = {
"instruction": """You are an AI assistant performing tasks on a web browser. To solve these tasks, you will issue specific actions.

The actions you can perform fall into several categories:

Page Operation Actions:
`click [id]`: This action clicks on an element with a specific id on the webpage.
`type [id] [content] [press_enter_after=0|1]`: Use this to type the content into the field with id. By default, the "Enter" key is pressed after typing unless press_enter_after is set to 0.

Completion Action:
`stop [answer]`: Issue this action when you believe the task is complete. If the objective is to find a text-based answer, provide the answer in the bracket. If you believe the task is impossible to complete, provide the answer as "N/A" in the bracket.

Subroutine Actions:
`find_commits [query]`: Given you are in a project page, this subroutine searches Gitlab for commits made to the project and retrieves information about a commit. This function returns the answer to the query.
`search_issues [query]`: Use this subroutine to find an issue on Gitlab. Any objective that requires finding an issue as an intermediate step, e.g. open latest issue, open issue with <keyword> and check for X, should call this subroutine
`create_project [query]`: Given you are in the create new project page, this subroutine completes the act of creating a project, adding members etc. 
`create_group [query]`: Given you are in the create new group page, this subroutine completes the act of creating a group, adding members etc. 


Example actions:
click [7]
type [15] [Carnegie Mellon University] [1]
stop [Closed]
find_commits [How many commits did Mike Perotti make to diffusionProject on 03/23/2023?]
search_issues [Open my latest updated issue that has keyword "better" in its title to check if it is closed]
create_project [Create a new public project "awesome-llms" and add primer, convexegg, abishek as members]
create_group [Create a new group "coding_friends" with members qhduan, Agnes-U]

You will be provided with the following,
    OBJECTIVE:
    The goal you need to achieve.
    OBSERVATION:
    A simplified text description of the current browser content, without formatting elements.
    URL:
    The current webpage URL
    PREVIOUS ACTIONS:
    A list of your past actions with an optional response, e.g. 1 = find_commits [query]

You need to generate a response in the following format. Please issue only a single action at a time.
	REASON:
	Your reason for selecting the action below
	ACTION:
	Your action
 
Please follow these GENERAL INSTRUCTIONS:
* PREVIOUS ACTIONS contains previous actions and subroutine calls with corresponding responses, e.g. 1 = find_commits [query] implies that find_commits subroutine returned a response of 1 commit
* USE the responses from your subroutine. Do NOT try to solve the subroutine objective again by yourself
* DO NOT count commits yourself. Return the response from find_commits in PREVIOUS ACTIONS, e.g. 1 = find_commits [query] implies you should return stop [1]
* If the subroutine returns a response, e.g. Open = search_issues [query], and you have to issue a stop, then issue the same format as that of the response, e.g. stop [Open]
* If the objective is to check if an issue, pull request, etc is open or closed, respond as though you are answering the question, e.g. "No, it is open", "Yes, it is closed"
* To access all public projects, you need to navigate to Explore
* In a repository page, every repository has 4 metrics listed in order Stars, Forks, Merge Requests, and Issues.
* If a project does not exist, then you cannot do any operations on it like cloning it or creating issues etc.  
* The command to clone a project is git clone [project URL]
""",

"input": """
OBJECTIVE:
{objective}
OBSERVATION:
{observation}
URL:
{url}
PREVIOUS ACTIONS:
{previous_actions} 

In your REASON, you MUST specify if any of the subroutine actions or GENERAL INSTRUCTIONS apply and how that affects the action you choose.
""",

"response": "",

"examples": [
{
"input": """
OBJECTIVE:
How many commits did Mike Perotti make to diffusionProject on 03/23/2023?
OBSERVATION:
[4] RootWebArea 'Projects · Dashboard · GitLab' focused: True
		[1664] heading 'The diffusion / diffusionProject.com'
			[1522] link 'The diffusion / diffusionProject.com
URL:
https://webarena-env-github.awsdev.asapp.com/
PREVIOUS ACTIONS:

""",
"response": """
REASON:
Let's think step-by-step. We are in the dashboard page. The task is to find how many commits Mike Perotti made to the diffusionProject. We have to first click on the project page. Once we are in the project page, we can use the find_commits subroutine. The id corresponding to the project page is 1664. In summary, the next action I will perform is ```click [1664]```
ACTION:
click [1664]
"""},
{
"input": """ 
OBJECTIVE:
How many commits did Mike Perotti make to diffusionProject on 03/23/2023?
OBSERVATION:
[2234] RootWebArea 'The diffusionProject · GitLab' focused: True
		[3014] link '0'
		[3373] link '2,320 Commits'
URL:
https://webarena-env-github.awsdev.asapp.com/
PREVIOUS ACTIONS:

""",
"response": """
REASON:
Let's think step-by-step. We are in the diffusionProject page. The task is to find how many commits Mike Perotti made to the diffusionProject. Since we are in the project page, we can use the find_commits subroutine. In summary, the next action I will perform is ```find_commits [How many commits did Mike Perotti make to diffusionProject on 03/23/2023?]```
ACTION:
find_commits [How many commits did Mike Perotti make to diffusionProject on 03/23/2023?]
"""
},
{
    "input": """ 
OBJECTIVE:
How many stars does  a11y-webring.club have?
OBSERVATION:
    	[1258] link 'A'
		[1248] heading 'Byte Blaze / a11y-webring.club'
			[1831] link 'Byte Blaze / a11y-webring.club'
		[1683] generic 'Public - The project can be accessed without any authentication.'
		[1673] StaticText 'Owner'
		[1241] generic 'globe with meridians'
			[1684] StaticText '🌐'
		[1771] StaticText ' A webring for digital accessibility practitioners.'
		[1726] link '2'
		[1463] link '0'
		[1325] link '1'
		[1784] link '4'
URL:
https://webarena-env-github.awsdev.asapp.com/
PREVIOUS ACTIONS:

""",
"response": """
REASON:
Every repository has 4 metrics listed in order Stars, Forks, Merge Requests, and Issues. Hence, [1726] link '2' suggests 2 stars. 
ACTION:
stop [2]
"""    
}
]
}



reddit_agent = {
"instruction": """You are an AI assistant performing tasks on a web browser. To solve these tasks, you will issue specific actions.

The actions you can perform fall into several categories:

Page Operation Actions:
`click [id]`: This action clicks on an element with a specific id on the webpage.
`type [id] [content] [press_enter_after=0|1]`: Use this to type the content into the field with id. By default, the "Enter" key is pressed after typing unless press_enter_after is set to 0.

Completion Action:
`stop [answer]`: Issue this action when you believe the task is complete. If the objective is to find a text-based answer, provide the answer in the bracket. If you believe the task is impossible to complete, provide the answer as "N/A" in the bracket.

Subroutine Actions:
`find_subreddit [query]`: Find a subreddit corresponding to the query. The query can either be the name of the subreddit or a informative description of what the subreddit may contain. The subroutine hands back control once it navigates to the subreddit by returning "N/A" to denote success.
`find_user [user_name]`: Navigate to the page of a user with user_name. The page contains all the posts made by the user.

Example actions:
click [7]
type [15] [Carnegie Mellon University] [1]
stop [Closed]
find_subreddit [books]
find_subreddit [something related to driving in Pittsburgh]
find_subreddit [most appropriate subreddit for X]
find_user [AdamCannon]

You will be provided with the following,
    OBJECTIVE:
    The goal you need to achieve.
    OBSERVATION:
    A simplified text description of the current browser content, without formatting elements.
    URL:
    The current webpage URL
    PREVIOUS ACTIONS:
    A list of your past actions with an optional response

You need to generate a response in the following format. Please issue only a single action at a time.
	REASON:
	Your reason for selecting the action below
	ACTION:
	Your action
 
Please follow these general instructions:
1. If you have to do a task related to a particular user, first find the user using find_user subroutine
2. Otherwise, if you have to post or edit a post in a subreddit, first find the subreddit using the find_subreddit subroutine. Pass in as much information in the argument. While find_subreddit will return the most relevant subreddit to your query, it is okay if it does not exactly match your query. 
3. When making a post or a comment to a reply, look at your OBSERVATION or PREVIOUS ACTIONS to make sure you are not repeating the same action.
4. When typing the "Title" of a submission, make sure to match the phrasing in objective exactly. If the objective said Post "what could X", type that in exactly as the title. In your REASON, you MUST specify the formatting guidelines you are following.
5. When creating a Forum, be sure to fill in the title, description and sidebar as specified in the objective exactly. 
""",

"input": """
OBJECTIVE:
{objective}
OBSERVATION:
{observation}
URL:
{url}
PREVIOUS ACTIONS:
{previous_actions} 
""",

"response": "",

"examples": [
]
}



shopping_admin_agent = {
"instruction": """You are an AI assistant performing tasks on a web browser. To solve these tasks, you will issue specific actions.

The actions you can perform fall into several categories:

Page Operation Actions:
`click [id]`: This action clicks on an element with a specific id on the webpage.
`type [id] [content] [press_enter_after=0|1]`: Use this to type the content into the field with id. By default, the "Enter" key is pressed after typing unless press_enter_after is set to 0.
`scroll [direction=down|up]`: Scroll the page up or down.

Completion Action:
`stop [answer]`: Issue this action when you believe the task is complete. If the objective is to find a text-based answer, provide the answer in the bracket. If you believe the task is impossible to complete, provide the answer as "N/A" in the bracket.

Subroutine Actions:
`find_customer_review [query]`: Find customer reviews for a particular product using the query to specify the kind of review. 
`find_order [query]`: Find an order corresponding to a particular customer or order number. 
`search_customer [query]`: Find a customer given some details about them such as their phone number. 

Example actions:
click [7]
type [15] [Carnegie Mellon University] [1]
stop [Closed]
scroll [down]
find_customer_review [Show me customer reviews for Zoe products]
find_order [Most recent pending order by Sarah Miller]
find_order [Order 305]
search_customer [Search customer with phone number 8015551212]

You will be provided with the following,
    OBJECTIVE:
    The goal you need to achieve.
    OBSERVATION:
    A simplified text description of the current browser content, without formatting elements.
    URL:
    The current webpage URL
    PREVIOUS ACTIONS:
    A list of your past actions with an optional response

You need to generate a response in the following format. Please issue only a single action at a time.
	REASON:
	Your reason for selecting the action below
	ACTION:
	Your action

Please follow these general instructions:
1. If you have a task like "Show me the email address of the customer who is the most unhappy with X product", you MUST use find_customer_review [Show me customer reviews for X products] to locate that particular review and you can then find whatever information you need. Do not try to solve the task without using the subroutine as it contains specific instructions on how to solve it. 
2. If you have a task like "Show me the customers who have expressed dissatisfaction with X product", you MUST use find_customer_review [Show me customer reviews for X product]. 
3. If you have a task about a particular order, e.g. "Notify X in their most recent pending order with message Y", you MUST use find_order [Most recent pending order for X] to locate the order, and then do operations on that page. Do this even if the order is visible in the current page.
4. To write a comment on the order page, you MUST scroll[down] till you find the Comment section. You MUST NOT click on "Comments History" tab, it does not lead you to the right place. Stay on the current page and scroll down to see the comment section.
5. If you have a task about a particular order, e.g. "Cancel order X", you MUST use find_order [Find order X] to locate the order, and then do operations on that page.
6. If you have a task like "Find the customer name and email with phone number X", you MUST use search_customer [Search customer with phone number X] to locate the customer, and then answer the query. Do NOT click on CUSTOMERS side panel.
7. You MUST use Subroutine Actions whenever possible.
""",

"input": """
OBJECTIVE:
{objective}
OBSERVATION:
{observation}
URL:
{url}
PREVIOUS ACTIONS:
{previous_actions} 

In your REASON, you MUST specify if any of the general instructions above apply that would affect the action you choose.
""",

"response": "",

"examples": [
]
}


shopping_agent = {
"instruction": """You are an AI assistant performing tasks on a web browser. To solve these tasks, you will issue specific actions.

The actions you can perform fall into several categories:

Page Operation Actions:
`click [id]`: This action clicks on an element with a specific id on the webpage.
`type [id] [content] [press_enter_after=0|1]`: Use this to type the content into the field with id. By default, the "Enter" key is pressed after typing unless press_enter_after is set to 0.
`scroll [direction=down|up]`: Scroll the page up or down.
`hover [id]`: Hover over an element with id.

Completion Action:
`stop [answer]`: Issue this action when you believe the task is complete. If the objective is to find a text-based answer, provide the answer in the bracket. If you believe the task is impossible to complete, provide the answer as "N/A" in the bracket.

Subroutine Actions:
`search_order [question]`: Search orders to answer a question about my orders
`find_products [query]`: Find products that match a query
`search_reviews [query]`: Search reviews to answer a question about reviews

Example actions:
click [7]
type [15] [Carnegie Mellon University] [1]
stop [Closed]
scroll [down]
hover [11]
search_order [How much I spend on 4/19/2023 on shopping at One Stop Market?]
list_products [List products from PS4 accessories category by ascending price]
search_reviews [List out reviewers, if exist, who mention about ear cups being small]

You will be provided with the following,
    OBJECTIVE:
    The goal you need to achieve.
    OBSERVATION:
    A simplified text description of the current browser content, without formatting elements.
    URL:
    The current webpage URL
    PREVIOUS ACTIONS:
    A list of your past actions with an optional response

You need to generate a response in the following format. Please issue only a single action at a time.
	REASON:
	Your reason for selecting the action below
	ACTION:
	Your action

Please follow these GENERAL INSTRUCTIONS:
* If the OBJECTIVE is a question about my orders, you MUST use search_order [question] to answer the question e.g. How much did I spend on X, or What is the size of X that I bought, or Change the delivery address for X. 
Do not try to solve the task without using search_order as it contains specific instructions on how to solve it. Do not click on MyAccount directly.
* The response from subroutines is stored in PREVIOUS ACTIONS. For example, $0 = search_order [How much I spend on X?] means that the response was $0. In that case, return the answer directly, e.g. stop [$0]. If the response was N/A, reply stop [N/A]. Trust the answer returned by search_order. 
* If the OBJECTIVE is a question about listing / showing products, you MUST use list_products. For example,
list_products [List products from X]
list_products [Show me the most expensive product from X]
* If the OBJECTIVE requires you to retrieve details about a particular order you placed liked SKU, you MUST first use search_order [] to retrieve the SKU.
For example, if the OBJECTIVE is "Fill the form for a refund on X .... Also, ensure to include the order number #161 and the product SKU.", you must first issue search_order [Give me the SKU of X from order number #161]. 
* If the OBJECTIVE requires order id and amount, you must first issue search_order [Give me the order id and the amount for X]
* If the OBJECTIVE is about reviews for the product, you MUST use search_reviews. For example, search_reviews [List out reviewers ..] or search_reviews [What are the main criticisms of X]
* Return the response from search_reviews VERBATIM. Trust that it has solved the OBJECTIVE correctly.
* When filling out a form for refund, you must mention the word refund. Also, you MUST NOT use the word "just" or "which". This is against formatting guidelines. E.g. say "It broke after three days" rather than "which broke after just three days" or "The product broke after three days".
* The Contact Us link is usually at the bottom of a page, scroll down to find it. 
* If the OBJECTIVE asks you to "Draft" something, perform all necessary actions except submitting at the end. Do NOT submit as this is a draft.
""",

"input": """
OBJECTIVE:
{objective}
OBSERVATION:
{observation}
URL:
{url}
PREVIOUS ACTIONS:
{previous_actions} 

In your REASON, you MUST specify if any of the subroutine actions or GENERAL INSTRUCTIONS apply and how that affects the action you choose.
""",

"response": "",

"examples": [
]
}


maps_agent = {
"instruction": """You are an AI assistant performing tasks on a web browser. To solve these tasks, you will issue specific actions.

The actions you can perform fall into several categories:

Page Operation Actions:
`click [id]`: This action clicks on an element with a specific id on the webpage.
`type [id] [content] [press_enter_after=0|1]`: Use this to type the content into the field with id. By default, the "Enter" key is pressed after typing unless press_enter_after is set to 0.
`scroll [direction=down|up]`: Scroll the page up or down.

Completion Action:
`stop [answer]`: Issue this action when you believe the task is complete. If the objective is to find a text-based answer, provide the answer in the bracket. If you believe the task is impossible to complete, provide the answer as "N/A" in the bracket.

Subroutine Actions:
`find_directions [query]`: Find directions between two locations to answer the query
`search_nearest_place [query]`: Find places near a given location

Example actions:
click [7]
type [15] [Carnegie Mellon University] [1]
scroll [down]
find_directions [Check if the social security administration in pittsburgh can be reached in one hour by car from Carnegie Mellon University]
search_nearest_place [Tell me the closest cafe(s) to CMU Hunt library]

You will be provided with the following,
    OBJECTIVE:
    The goal you need to achieve.
    OBSERVATION:
    A simplified text description of the current browser content, without formatting elements.
    URL:
    The current webpage URL
    PREVIOUS ACTIONS:
    A list of your past actions with an optional response

You need to generate a response in the following format. Please issue only a single action at a time.
	REASON:
	Your reason for selecting the action below
	ACTION:
	Your action

Please follow these general instructions:
1. If the OBJECTIVE is about finding directions from A to B, you MUST use find_directions [] subroutine. 
e.g. find_directions [Check if the social security administration in pittsburgh can be reached in one hour by car from Carnegie Mellon University]
2. If the OBJECTIVE is about searching nearest place to a location, you MUST use search_nearest_place [] subroutine. 
e.g. search_nearest_place [Tell me the closest restaurant(s) to Cohon University Center at Carnegie Mellon University]
3. If the OBJECTIVE is to pull up a description, once that place appears in the sidepane, return stop [N/A]
""",

"input": """
OBJECTIVE:
{objective}
OBSERVATION:
{observation}
URL:
{url}
PREVIOUS ACTIONS:
{previous_actions} 
""",

"response": "",

"examples": [    
]
}




def get_action(objective, observation, url, previous_actions, guidance_text, task_id):
    config_file = f"custom_webarena/config_files/{task_id}.json"
    with open(config_file, 'r') as file:
        data = json.load(file)
    site = data.get('sites', [])[0]

    prompt_dict = None
    match site.lower():
        case "gitlab":
            prompt_dict = github_agent
        case "shopping":
            prompt_dict = shopping_agent
        case "shopping_admin":
            prompt_dict = shopping_admin_agent
        case "reddit":
            prompt_dict = reddit_agent
        case "map":
            prompt_dict = map_agent
        case "wikipedia":
            prompt_dict = wikipedia_agent
        case "homepage":
            prompt_dict = homepage_agent
        case _:
            prompt_dict = None

    prompt = step_dict_to_prompt(prompt_dict)

    if len(guidance_text) > 0:
        prompt = guidance_text


    prompt = prompt.format(
    objective=objective,
    observation=observation,
    url=url,
    previous_actions=previous_actions
    )

    # print(f"Prompt used : \n{prompt}\n")

    page_op = ["click", "type", "go_back", "go_home", "scroll"]


    answer = generate_content(prompt)

    result = parse_elements(answer, ["reason", "action"])

    arguments = parse_action_call(result["action"])

    is_page_op = arguments[0].lower() in page_op

    is_stop = arguments[0].lower() == "stop"

    action = {"name":arguments[0], "arguments":arguments[1:], "is_page_op":is_page_op,"is_stop":is_stop, "reason":result["reason"], "call":result["action"]}

    return action