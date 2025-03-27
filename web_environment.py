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

	def load(self,obs):
		self.current_url = ""
		# Temporary only used for basic testing
		self.current_observation = obs