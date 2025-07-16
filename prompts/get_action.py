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


input_output = """
You will be provided with the following,
    OBJECTIVE:
    The current goal you need to complete.
    DESCRIPTION:
    The description of the type of objective you need to complete (empty if the objective is self-explanatory)
    OBSERVATION:
    A simplified text description of the current browser content, without formatting elements.
    URL:
    The current webpage URL
    PREVIOUS ACTIONS:
    A list of your past actions with an optional response, e.g. find_commits [query], stop [2]

Generate an answer adhering strictly to the following YAML output format (CATEGORY in capital letters followed directly by a colon).
Please issue only a single action at a time.
	REASON:
	Your reason for selecting the action below
	ACTION:
	Your action
"""


site_instructions = {
"gitlab" : """* DO NOT count commits yourself. Return the response from find_commits in PREVIOUS ACTIONS, e.g. 1 = find_commits [query] implies you should return stop [1]
* If the subroutine returns a response, e.g. Open = search_issues [query], and you have to issue a stop, then issue the same format as that of the response, e.g. stop [Open]
* If the objective is to check if an issue, pull request, etc is open or closed, respond as though you are answering the question, e.g. "No, it is open", "Yes, it is closed"
* To access all public projects, you need to navigate to Explore
* In a repository page, every repository has 4 metrics listed in order Stars, Forks, Merge Requests, and Issues.
* If a project does not exist, then you cannot do any operations on it like cloning it or creating issues etc.  
* The command to clone a project is git clone [project URL]""",
"reddit" : """*. If you have to do a task related to a particular user, first find the user using find_user subroutine
*. Otherwise, if you have to post or edit a post in a subreddit, first find the subreddit using the find_subreddit subroutine. Pass in as much information in the argument. While find_subreddit will return the most relevant subreddit to your query, it is okay if it does not exactly match your query. 
*. When making a post or a comment to a reply, look at your OBSERVATION or PREVIOUS ACTIONS to make sure you are not repeating the same action.
*. When typing the "Title" of a submission, make sure to match the phrasing in objective exactly. If the objective said Post "what could X", type that in exactly as the title. In your REASON, you MUST specify the formatting guidelines you are following.
*. When creating a Forum, be sure to fill in the title, description and sidebar as specified in the objective exactly. 
""",
"shopping_admin": """* If you have a task like "Show me the email address of the customer who is the most unhappy with X product", you MUST use find_customer_review [Show me customer reviews for X products] to locate that particular review and you can then find whatever information you need. Do not try to solve the task without using the subroutine as it contains specific instructions on how to solve it. 
* If you have a task like "Show me the customers who have expressed dissatisfaction with X product", you MUST use find_customer_review [Show me customer reviews for X product]. 
* If you have a task about a particular order, e.g. "Notify X in their most recent pending order with message Y", you MUST use find_order [Most recent pending order for X] to locate the order, and then do operations on that page. Do this even if the order is visible in the current page.
* To write a comment on the order page, you MUST scroll[down] till you find the Comment section. You MUST NOT click on "Comments History" tab, it does not lead you to the right place. Stay on the current page and scroll down to see the comment section.
* If you have a task about a particular order, e.g. "Cancel order X", you MUST use find_order [Find order X] to locate the order, and then do operations on that page.
* If you have a task like "Find the customer name and email with phone number X", you MUST use search_customer [Search customer with phone number X] to locate the customer, and then answer the query. Do NOT click on CUSTOMERS side panel.
* You MUST use Subroutine Actions whenever possible.""",
"shopping" : """* If the OBJECTIVE is a question about my orders, you MUST use search_order [question] to answer the question e.g. How much did I spend on X, or What is the size of X that I bought, or Change the delivery address for X. 
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
"map" : """* If the OBJECTIVE is about finding directions from A to B, you MUST use find_directions [] subroutine. 
e.g. find_directions [Check if the social security administration in pittsburgh can be reached in one hour by car from Carnegie Mellon University]
* If the OBJECTIVE is about searching nearest place to a location, you MUST use search_nearest_place [] subroutine. 
e.g. search_nearest_place [Tell me the closest restaurant(s) to Cohon University Center at Carnegie Mellon University]
* If the OBJECTIVE is to pull up a description, once that place appears in the sidepane, return stop [N/A]
"""
}

examples = [
("gitlab" , """"
### Input:

Objective:
How many stars does  a11y-webring.club have?
Observation:
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
Url:
https://webarena-env-github.awsdev.asapp.com/
Previous Actions:

### Response:

Reason:
Every repository has 4 metrics listed in order Stars, Forks, Merge Requests, and Issues. Hence, [1726] link '2' suggests 2 stars. 
Action:
stop [2]
"""),

("gitlab", """
 ### Input:

Objective:
How many commits did Mike Perotti make to diffusionProject on 03/23/2023?
Observation:
[4] RootWebArea 'Projects · Dashboard · GitLab' focused: True
		[1664] heading 'The diffusion / diffusionProject.com'
			[1522] link 'The diffusion / diffusionProject.com
Url:
https://webarena-env-github.awsdev.asapp.com/
Previous Actions:

 ### Response:
 
Reason:
Let's think step-by-step. We are in the dashboard page. The task is to find how many commits Mike Perotti made to the diffusionProject. We have to first click on the project page. Once we are in the project page, we can use the find_commits subroutine. The id corresponding to the project page is 1664. In summary, the next action I will perform is ```click [1664]```
Action:
click [1664]""")
]


def get_action(objective, description, observation, url, previous_actions, guidance_text, relevant_policies, is_root, site=None, rec_nb=0):
    subroutine_actions_prompt = "\n" + "\n".join([f"{name} [query] : {description}" for (name, description) in relevant_policies])

    root_examples = "Here are a some examples of actions:" + "\n\n".join([c for (_,c) in examples]) if is_root else ""

    get_action_prompt = f"""
You are an AI assistant performing actions to solve tasks on a web browser.

The actions you can perform fall into several categories:

- Page Operation Actions:
{page_operations}

{"- Subroutine Actions:" + subroutine_actions_prompt if is_root else ""}

- Stop Action:
`stop [answer]`: To stop interaction and return response. Present your answer within the brackets . If the task doesn’t require a textual answer or appears insurmountable, indicate ‘N/A’ and additional reasons and all relevant information you gather as the answer . E.g. , ‘stop [5h 47min]’

Here are some example actions:

{example_page_operation}
{example_subroutines if not is_root else ""}

{input_output}

Please follow these general instructions:
{site_instructions[site] if is_root and (not (site is None)) else guidance_text}

{root_examples}

    
Input:

OBJECTIVE:
{objective}
DESCRIPTON:
{description}
OBSERVATION:
{observation}
URL:
{url}
PREVIOUS ACTIONS:
{previous_actions}
    """

# {"* A subroutine is a high-level function used to perform long-range tasks. Use them as an abstraction of multiple page operations." if is_root else ""}
# {"* Use subroutines as much as possible when fitting." if is_root else ""}
# * You do not have access to external resources. Limit yourself to the content of the current webpage.
# * Always refer to specific elements in the page by their ID and not by their name when using page operation actions.


    # print(get_action_prompt)

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
    except Exception as e:
        if rec_nb > 3:
            return None

        print(f"An error occured in get_action: {e}")
        return get_action(objective, description, observation, url, previous_actions, guidance_text, relevant_policies, is_root, site, rec_nb=rec_nb+1)
