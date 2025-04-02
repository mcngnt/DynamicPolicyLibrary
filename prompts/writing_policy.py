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


def write_policy(task_name, task_description, arguments, trajectory, critique, previous_guidance):
    writing_prompt = f"""
    {writing_system_prompt}
    Task name : {task_name}
    Task description : "{task_description}"
    Query with which the task was performed : {arguments}
    All the actions and observations from the last round : {trajectory}
    Critique : {critique}
    Guidance text from the last round : {previous_guidance}
    """

    answer = generate_content(writing_prompt)

    # Return only generated policy from answer

    result = parse_elements(answer, ["explain", "plan", "guidance"])

    result["guidance"] += "\nPlease, use ONLY page operation and no subroutine actions."

    return result


# ==== Prompt testing ===


my_task_name = """
search_nearest_place
"""

my_task_description = """
This Maps subroutine finds places near a given location.
"""

my_query = """
Tell me all international airports within a driving distance of 30 km to Carnegie Art Museum
"""

my_critique = """
The task was a failure. The agent failed tu use OpenStreetMap to find the nearest airports, even tough the task is possible.
SUCCESS : 0
"""

my_previous_guidance = """
Please follow these instructions to solve the subtask:

* For searches that refer to CMU, e.g. "find cafes near CMU Hunt Library" a. You have to first center your map around a location. If you have to find cafes near CMU Hunt Library, the first step is to make sure the map is centered around Carnegie Mellon University. To do that, first search for Carnegie Mellon University and then click [ ] on a list of location that appears. You MUST click on the Carnegie Mellon University location to center the map. Else the map will not centered. E.g click [646] b. Now that your map is centered around Carnegie Mellon University, directly search for "cafes near Hunt Library". Do not include the word CMU in the search item. The word CMU cannot be parsed by maps and will result in an invalid search. c. When your search returns a list of elements, return them in a structured format like stop [A, B, C]
* For searches that don't refer to CMU a. No need to center the map. Directly search what is specified in OBJECTIVE, e. g. "bars near Carnegie Music Hall" b. When your search returns a list of elements, return them in a structured format like stop [A, B, C]
* Be sure to double check whether the OBJECTIVE has CMU or not and then choose between instruction 1 and 2.
* Remember that the word CMU cannot be typed in the search bar as it cannot be parsed by maps.
* Remember that if you want to center your map around Carnegie Mellon University , you have to click on it after you search for it. Check your PREVIOUS ACTIONS to confirm you have done so, e.g. click [646] should be in the previous actions.
"""

my_trajectory = """
        {
            "objective": "Tell me the full address of all international airports that are within a driving distance of 30 km to Carnegie Art Museum",
            "url": "http://ec2-3-131-244-37.us-east-2.compute.amazonaws.com:3000/search?query=Carnegie%20Art%20Museum#map=19/40.44365/-79.94922",
            "observation": "Tab 0 (current): Carnegie Art Museum | OpenStreetMap\n\n[1] RootWebArea 'Carnegie Art Museum | OpenStreetMap' focused: True\n\t[36] heading 'OpenStreetMap logo OpenStreetMap'\n\t\t[41] link 'OpenStreetMap logo OpenStreetMap'\n\t\t\t[44] img 'OpenStreetMap logo'\n\t[402] link 'Edit'\n\t[403] button ''\n\t[373] link 'History'\n\t[374] link 'Export'\n\t[407] link 'GPS Traces'\n\t[408] link 'User Diaries'\n\t[409] link 'Communities'\n\t[410] link 'Copyright'\n\t[411] link 'Help'\n\t[412] link 'About'\n\t[382] link 'Log In'\n\t[383] link 'Sign Up'\n\t[12] textbox 'Search' focused: True required: False\n\t\t[522] StaticText 'Carnegie Art Museum'\n\t[516] button 'Go'\n\t[503] link 'Find directions between two points'\n\t[619] heading 'Search Results'\n\t[622] button 'Close'\n\t[617] heading 'Results from OpenStreetMap Nominatim'\n\t\t[624] link 'OpenStreetMap Nominatim'\n\t[631] StaticText 'Museum '\n\t[632] link 'Carnegie Museum of Art, South Craig Street, North Oakland, Pittsburgh, Allegheny County, 15213, United States'\n\t[629] link 'More results'\n\t[23] generic 'Zoom In Zoom Out Show My Location Layers Share 20 m 50 ft \u00a9 OpenStreetMap contributors \u2665 Make a Donation. Website and API terms'\n\t\t[27] link 'Zoom In'\n\t\t[28] link 'Zoom Out'\n\t\t[30] button 'Show My Location'\n\t\t[32] link 'Layers'\n\t\t[296] link ''\n\t\t[34] link 'Share'\n\t\t[298] link ''\n\t\t[300] link ''\n\t\t[614] StaticText '20 m'\n\t\t[615] StaticText '50 ft'\n\t\t[308] StaticText '\u00a9 '\n\t\t[309] link 'OpenStreetMap contributors'\n\t\t[310] StaticText ' \u2665 '\n\t\t[311] link 'Make a Donation'\n\t\t[312] StaticText '. '\n\t\t[313] link 'Website and API terms'",
            "previous_actions": [],
            "previous_responses": [],
            "previous_reasons": [],
            "action": "type [12] [Carnegie Art Museum] [1]",
            "reason": "To begin the task of finding international airports within a driving distance of 30 km to the Carnegie Art Museum, it is necessary to first search for the Carnegie Art Museum to ensure the map is centered around this location. This is a foundational step before proceeding to search for airports.",
            "done": false,
            "reward": 0.0,
            "success": 0.0,
            "num_actions": 2
        },
        {
            "objective": "search_nearest_place [Tell me all international airports within a driving distance of 30 km to Carnegie Art Museum]",
            "url": "http://ec2-3-131-244-37.us-east-2.compute.amazonaws.com:3000/search?query=Carnegie%20Art%20MuseCarnegie%20Art%20Museumum#map=19/40.44365/-79.94922",
            "observation": "Tab 0 (current): Carnegie Art MuseCarnegie Art Museumum | OpenStreetMap\n\n[1] RootWebArea 'Carnegie Art MuseCarnegie Art Museumum | OpenStreetMap' focused: True\n\t[36] heading 'OpenStreetMap logo OpenStreetMap'\n\t\t[41] link 'OpenStreetMap logo OpenStreetMap'\n\t\t\t[44] img 'OpenStreetMap logo'\n\t[402] link 'Edit'\n\t[403] button ''\n\t[373] link 'History'\n\t[374] link 'Export'\n\t[407] link 'GPS Traces'\n\t[408] link 'User Diaries'\n\t[409] link 'Communities'\n\t[410] link 'Copyright'\n\t[411] link 'Help'\n\t[412] link 'About'\n\t[382] link 'Log In'\n\t[383] link 'Sign Up'\n\t[12] textbox 'Search' focused: True required: False\n\t\t[649] StaticText 'Carnegie Art MuseCarnegie Art Museumum'\n\t[516] button 'Go'\n\t[503] link 'Find directions between two points'\n\t[660] heading 'Search Results'\n\t[663] button 'Close'\n\t[658] heading 'Results from OpenStreetMap Nominatim'\n\t\t[665] link 'OpenStreetMap Nominatim'\n\t[669] StaticText 'No results found'\n\t[23] generic 'Zoom In Zoom Out Show My Location Layers Share 20 m 50 ft \u00a9 OpenStreetMap contributors \u2665 Make a Donation. Website and API terms'\n\t\t[27] link 'Zoom In'\n\t\t[28] link 'Zoom Out'\n\t\t[30] button 'Show My Location'\n\t\t[32] link 'Layers'\n\t\t[296] link ''\n\t\t[34] link 'Share'\n\t\t[298] link ''\n\t\t[300] link ''\n\t\t[655] StaticText '20 m'\n\t\t[656] StaticText '50 ft'\n\t\t[308] StaticText '\u00a9 '\n\t\t[309] link 'OpenStreetMap contributors'\n\t\t[310] StaticText ' \u2665 '\n\t\t[311] link 'Make a Donation'\n\t\t[312] StaticText '. '\n\t\t[313] link 'Website and API terms'",
            "previous_actions": [],
            "previous_responses": [],
            "previous_reasons": [],
            "action": "stop [N/A]",
            "reason": "The current webpage is OpenStreetMap focused on the Carnegie Art Museum, but it does not provide the functionality to search for international airports within a specific driving distance. To find international airports within 30 km of the Carnegie Art Museum, a more suitable platform with such specific search capabilities, like Google Maps, would be needed. Since I cannot navigate to or interact with external websites or change the search parameters within this environment, I cannot complete the task as described."
        },
"""


def get_my_writing_answer():
    return write_policy(my_task_name, my_task_description, my_query, my_trajectory, my_critique, my_previous_guidance)




# Result with gemini-2.0-flash with previous guidance text on failed trajectory

# Explain: The agent didn't follow the instructions properly. It typed "Carnegie Art Museum" and then immediately stopped, claiming the platform doesn't allow searching within a driving distance. However, the instructions explicitly state to center the map first and then search for the specific request. The critique reinforces that the task is indeed possible within the environment. The guidance wasn't sufficient because it didn't explicitly break down the process of searching for a location before searching for nearby places.

# Plan:
# 1. First, center the map around the location mentioned in the query (e.g., Carnegie Art Museum). This might involve typing the location in the search bar and selecting it from the search results.
# 2. Once the map is centered, use the `search_nearest_place` tool to find the desired places (e.g., international airports) within the specified distance.
# 3. Extract the full address of each found place.
# 4. If no results are found, consider expanding the search radius or rephrasing the query.

# Guidance text: "To effectively use the `search_nearest_place` tool, follow these steps:

# 1. **Centering the Map:** The first crucial step is to center the map on the initial location specified in the objective (e.g., Carnegie Art Museum). This ensures the search for nearby places is relevant to the correct area.
#    *   Type the name of the location (e.g., "Carnegie Art Museum") in the search bar.
#    *   From the list of search results that appear, **select the correct location to center the map.**  Confirm that you have clicked on the location link. This step is critical; otherwise, the map will not be properly centered.
# 2. **Using `search_nearest_place`**: Once the map is centered, use the search_nearest_place tool . The tool will use the centered location as its starting point.
# 3. **Extracting Information**: Examine the results displayed on the map and identify the names and full addresses of the requested places (e.g., international airports).
# 4. **No Results**: If no results are immediately visible, try zooming out slightly or adjusting the search query (e.g., broadening the search terms, increasing the search radius).  Consider that there might genuinely be no places matching the criteria within the immediate vicinity.
# 5. **Specific place names**: When the OBJECTIVE contains names of specific places, type the entire name in the search box."


# The model does not understand how the policy stack work and recursively call itself






# Result with gemini-2.0-flash without previous guidance text
# Explain: The agent successfully completed the task. The guidance provided in previous rounds was sufficient. No changes are needed.

# Plan:
# 1) Start by navigating to the "My Account" section.
# 2) From "My Account", go to "My Orders" to view order history.
# 3) Navigate through the pages of order history to find the relevant time period (Jan 2023).
# 4) Once the order is found, view the order details to find the fake tree and its price configuration.
# 5) Stop and return the price configuration.

# Guidance text: "To find the price configuration of an item you ordered:
# * First, navigate to 'My Account'.
# * Then, go to 'My Orders' to see your order history.
# * You might need to navigate through multiple pages to find the order from the specific time period you're interested in. Use the 'Page' links to browse.
# * Once you find the order, click 'View Order' to see the details.
# * Look for the specific item you're asking about and identify its price.
# * Finally, stop and return the price of the item."

# Overfitted trajectory to the task



# Result with gemini-2.0-flash with previous guidance text
# Explain: The current guidance text is quite comprehensive, covering most scenarios encountered during order searches. However, it lacks specific instructions on identifying the correct item within an order, especially when the order contains multiple items. Additionally, it could benefit from a clearer instruction on how to handle situations where the item name in the order only partially matches the query.

# Plan:
# 1. Add a step for identifying the correct item within the order details.
# 2. Provide guidance on how to handle partial item name matches.
# 3. Reinforce the importance of accurately extracting the price configuration from the item details.
# 4. Include a reminder to examine the quantity ordered if relevant to the query.

# Guidance text: "Please follow these GENERAL INSTRUCTIONS:

# * Navigate to My Account, then My Orders to access all orders.
# * The orders are sorted by descending date. Click on Page Next to go to a earlier date. Click on Page Previous to go to a earlier date. If you don't see an order for a date, and the first order on the page is after the date, the last order on the page is before the date, then it means there is no order for the date.
# * In your REASON, state what is the current range, what range you are looking for, and whether you should search for an earlier or a later date.
# * If you have to find the total amount you spent on orders that span multiple pages, use note [Spent $10 on 4/1/2024] to make a personal note before moving on to the next page. When you are done, you can look at PREVIOUS ACTIONS to find all notes.
# * When you are adding numbers, work out each addition step by step in REASON.
# * Use go_back to go back to a previous page from an order. But before you do, use note [ ] to make a note that you checked the page, e.g. note [Checked order on 11/29/2023, no picture frame.]
# * If you are in an order page and need to go back, issue go_back. Don't click on My Orders else you have to start from all over again.
# * Do not keep visiting the same order page over and over again! To prevent this, whenever you visit a page, always make a note. For example note [Nothing relevant purchased on September 29, 2022] See note [ ] to see what dates you have visit, and be sure to not visit that page again.
# * Once you are done visiting all the pages, return stop [answer] with the answer to the query.
# * If the question is how much did I spend on a date, and I didn't spend anything , return stop [$0]
# * If the status of an order shows cancelled, that means I did not spend that money
# * If you are asked to change the delivery address on an order, you can't. Reply stop [N/A]
# * When viewing order details, carefully examine the items listed to find the one that best matches the product described in the query.
# * If the item name only partially matches the query, consider other details in the description to confirm it's the correct item.
# * Accurately extract the price configuration for the identified item from the order details.
# * Check the quantity ordered if relevant to the query (e.g., "price per item")."


# Useless additions ? Perhaps because this trajectory was a success



# Result with gemini-2.0-flash with only the first observation (homepage) and no guiding text nor query

# Explain: The agent is currently on the home page of the "One Stop Market" website. To search orders, it needs to navigate to the "My Account" section first. The guidance should instruct the agent to find and click the "My Account" link.

# Plan:
# 1. Find the "My Account" link.
# 2. Click on the "My Account" link to access order information.
# 3. Provide general guidance on how to proceed after reaching the "My Account" page (e.g., looking for order history or order search options).

# Guidance text: "To search your orders, first locate and click on the 'My Account' link. Once you are in the 'My Account' section, look for options such as 'Order History' or a search bar specifically for orders to find the information you need."




















# Specify agent
# Policy examples
# Retrieved policies ? 

# Rounds structure
	# - Old policy
	# - Output from previous round (Critique)
	# - Global instruction
	# - Current subtask( like the automatic curriculum) / general policy need
	# - Trajectory

# Ask for a rewrite
# "Explain (if applicable): Are there any steps missing in your plan? Why
#  does the code not complete the task? What does the chat log and
#  execution error imply?"

# General directives
# Give meaningful name to the policy
# Take into account existing policies
# Make it generic and reusable

# Format
# RESPONSE FORMAT:
#  Explain: ...
#  Plan:
#  1) ...
#  2) ...
#  3) ...
#  ...
#  Policy:
#  ...

