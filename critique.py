from utils import *



 # Plan progress assessment : Review critically why the plans have not been fulfilled or the objective achieved .
 # J ustify your assessment with detailed evidence drawn from the objective , observations , and actions taken
 # .
 # I temize the assessment using this format : ‘− plan [{plan id}]\n\t[{step
 # [{ concrete proof from
 # observation }] [{why milestone a
 # i ds taken
 # not successful}]\n\t[{
 # s t ep
 # i ds taken
 # f or this milestone }] [{concrete proof from
 # f or this milestone }]
 # observation }] [{why milestone b
 # not successful
 # }]\n\t . . . ’ .
 

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

Adhere to the following output format :
REVIEW:
Make a brief summary of all the actions taken as well as the final state of the webpage afterwards.
EXPLAIN:
Explain whether or not the actions taken were enough to fullfill the objective. Explain why it is a success or why is it a failure.
SUCCESS:
Output 1 if it is a succes (objective fullfilled), 0 if it is a failure (objective not fullfilled)
CRITIQUE:
If the task is a failure, explain what needs to be changed to become a success.
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

    result = parse_elements(answer, ["review", "explain", "success", "critique"])

    return result



# ==== Prompt testing ===

my_objective = """
Tell me the full address of all international airports that are within a driving distance of 30 km to Carnegie Art Museum
"""

my_observation = """
Tab 0 (current): Carnegie Art Museum | OpenStreetMap\n\n[1] RootWebArea 'Carnegie Art Museum | OpenStreetMap' focused: True\n\t[36] heading 'OpenStreetMap logo OpenStreetMap'\n\t\t[41] link 'OpenStreetMap logo OpenStreetMap'\n\t\t\t[44] img 'OpenStreetMap logo'\n\t[402] link 'Edit'\n\t[403] button ''\n\t[373] link 'History'\n\t[374] link 'Export'\n\t[407] link 'GPS Traces'\n\t[408] link 'User Diaries'\n\t[409] link 'Communities'\n\t[410] link 'Copyright'\n\t[411] link 'Help'\n\t[412] link 'About'\n\t[382] link 'Log In'\n\t[383] link 'Sign Up'\n\t[12] textbox 'Search' focused: True required: False\n\t\t[522] StaticText 'Carnegie Art Museum'\n\t[516] button 'Go'\n\t[503] link 'Find directions between two points'\n\t[619] heading 'Search Results'\n\t[622] button 'Close'\n\t[617] heading 'Results from OpenStreetMap Nominatim'\n\t\t[624] link 'OpenStreetMap Nominatim'\n\t[631] StaticText 'Museum '\n\t[632] link 'Carnegie Museum of Art, South Craig Street, North Oakland, Pittsburgh, Allegheny County, 15213, United States'\n\t[629] link 'More results'\n\t[23] generic 'Zoom In Zoom Out Show My Location Layers Share 20 m 50 ft \u00a9 OpenStreetMap contributors \u2665 Make a Donation. Website and API terms'\n\t\t[27] link 'Zoom In'\n\t\t[28] link 'Zoom Out'\n\t\t[30] button 'Show My Location'\n\t\t[32] link 'Layers'\n\t\t[296] link ''\n\t\t[34] link 'Share'\n\t\t[298] link ''\n\t\t[300] link ''\n\t\t[614] StaticText '20 m'\n\t\t[615] StaticText '50 ft'\n\t\t[308] StaticText '\u00a9 '\n\t\t[309] link 'OpenStreetMap contributors'\n\t\t[310] StaticText ' \u2665 '\n\t\t[311] link 'Make a Donation'\n\t\t[312] StaticText '. '\n\t\t[313] link 'Website and API terms'
"""

my_url = """
http://ec2-3-131-244-37.us-east-2.compute.amazonaws.com:3000/search?query=Carnegie%20Art%20Museum#map=19/40.44365/-79.94922
"""


my_previous_actions = """
type [12] [Carnegie Art Museum] [1]
"""


def get_my_critique():
    return get_critique(my_objective, my_observation, my_url, my_previous_actions)
