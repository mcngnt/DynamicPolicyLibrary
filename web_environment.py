from utils import *

base_actions = """
Page Operation Actions:
- click [ id ]: To click on an element with its numerical ID on the webpage. E.g. , ‘click [7] ’ If clicking on a specific element doesn ’ t trigger the transition to your desired web state , this is due to the element’s lack of interactivity or GUI visibility . In such cases, move on to interact with OTHER similar or relevant elements INSTEAD.
- type [ id ] [ content ] [ press enter after =0|1]: To type content into a field with a specific ID. By default , the ‘ Enter ’ key is pressed after typing unless ‘press enter after ’ is set to 0. E.g. , ‘type [15] [Carnegie Mellon University ] [1] ’ If you can ’ t find what you’re looking for on your first attempt , consider refining your search keywords by breaking them down or trying related terms.
- go_back : To return to the previously viewed page.
- note [ content ]: To take note of all important info w.r.t. completing the task to enable reviewing it later . E.g. , ‘note [Spent $10 on 4/1/2024] ’
- stop [ answer ]: To stop interaction and return response. Present your answer within the brackets . If the task doesn’t require a textual answer or appears insurmountable, indicate ‘N/A’ and additional reasons and all relevant information you gather as the answer . E.g. , ‘stop [5h 47min]’
- go_home: To return to the homepage where you can find other websites.
"""

class WebEnvironment:
	def __init__(self):
		self.current_url = ""
		self.current_observation = ""

	def observe(self):
		return 

	def interact(self, action_name, arguments=[]):
		action_call = print_action_call(action_name, arguments)

		prompt = f"""
		You are an AI web navigator. Based on the current state of the website and on an action performed on the page, you have to predict the new state of the webpage.

		Here are the available page actions :
		{base_actions}

		Here is the current state of the page :
		{self.current_observation}

		Here is the action performed :
		{action_call}

		Answer by giving the new state of the web page.
		"""

		self.current_observation = generate_content(prompt)

	def load(self,url):
		self.current_url = ""
		self.current_observation = """Tab 0 (current): OpenStreetMap\n\n[1] RootWebArea 'OpenStreetMap' focused: True\n\t[36] heading 'OpenStreetMap logo OpenStreetMap'\n\t\t[41] link 'OpenStreetMap logo OpenStreetMap'\n\t\t\t[44] img 'OpenStreetMap logo'\n\t[402] link 'Edit'\n\t[403] button ''\n\t[373] link 'History'\n\t[374] link 'Export'\n\t[407] link 'GPS Traces'\n\t[408] link 'User Diaries'\n\t[409] link 'Communities'\n\t[410] link 'Copyright'\n\t[411] link 'Help'\n\t[412] link 'About'\n\t[382] link 'Log In'\n\t[383] link 'Sign Up'\n\t[515] link 'Where is this?'\n\t[12] textbox 'Search' focused: True required: False\n\t[516] button 'Go'\n\t[503] link 'Find directions between two points'\n\t[466] heading 'Welcome to OpenStreetMap!'\n\t[469] button 'Close'\n\t[473] StaticText 'OpenStreetMap is a map of the world, created by people like you and free to use under an open license.'\n\t[474] StaticText 'Hosting is supported by '\n\t[475] link 'UCL'\n\t[477] link 'Fastly'\n\t[478] StaticText ', '\n\t[479] link 'Bytemark Hosting'\n\t[480] StaticText ', and other '\n\t[481] link 'partners'\n\t[482] StaticText '.'\n\t[485] link 'Learn More'\n\t[486] link 'Start Mapping'\n\t[23] generic 'Zoom In Zoom Out Show My Location Layers Share 50 km 50 mi \u00a9 OpenStreetMap contributors \u2665 Make a Donation. Website and API terms'\n\t\t[27] link 'Zoom In'\n\t\t[28] link 'Zoom Out'\n\t\t[30] button 'Show My Location'\n\t\t[32] link 'Layers'\n\t\t[296] link ''\n\t\t[34] link 'Share'\n\t\t[298] link ''\n\t\t[300] link ''\n\t\t[305] StaticText '50 km'\n\t\t[306] StaticText '50 mi'\n\t\t[308] StaticText '\u00a9 '\n\t\t[309] link 'OpenStreetMap contributors'\n\t\t[310] StaticText ' \u2665 '\n\t\t[311] link 'Make a Donation'\n\t\t[312] StaticText '. '\n\t\t[313] link 'Website and API terms'"""