from utils import *
from enum import Enum
import gymnasium as gym
import browsergym.core
from browsergym.utils.obs import flatten_axtree_to_str, flatten_dom_to_str, prune_html


# Page Operation Actions:
# - `click [ id ]`: To click on an element with its numerical ID on the webpage. E.g. , ‘click [7] ’ If clicking on a specific element doesn ’ t trigger the transition to your desired web state , this is due to the element’s lack of interactivity or GUI visibility . In such cases, move on to interact with OTHER similar or relevant elements INSTEAD.
# - `type [id] [content] [press enter after = 0|1]`: To type content into a field with a specific ID. By default , the ‘ Enter ’ key is pressed after typing unless ‘press enter after ’ is set to 0. E.g. , ‘type [15] [Carnegie Mellon University ] [1] ’ If you can ’ t find what you’re looking for on your first attempt , consider refining your search keywords by breaking them down or trying related terms.
# - `note [ content ]`: To take note of all important info w.r.t. completing the task to enable reviewing it later . E.g. , ‘note [Spent $10 on 4/1/2024] ’
# - `stop [ answer ]`: To stop interaction and return response. Present your answer within the brackets . If the task doesn’t require a textual answer or appears insurmountable, indicate ‘N/A’ and additional reasons and all relevant information you gather as the answer . E.g. , ‘stop [5h 47min]’
# - `go_home`: To return to the homepage where you can find other websites.

# goto(url: str)
#     Examples:
#         goto('http://www.example.com')

# go_back()
#     Examples:
#         go_back()

# fill(bid: str, value: str)
#     Examples:
#         fill('237', 'example value')

#         fill('45', 'multi-line\nexample')

#         fill('a12', 'example with "quotes"')

# click(bid: str, button: Literal['left', 'middle', 'right'] = 'left', modifiers: list[typing.Literal['Alt', 'Control', 'ControlOrMeta', 'Meta', 'Shift']] = [])
#     Examples:
#         click('a51')

#         click('b22', button='right')

#         click('48', button='middle', modifiers=['Shift'])


def print_gym_call(name, arguments):
	return f"""{name}({','.join([f"\'{arg}\'" for arg in arguments])})"""


class AvailableURL(Enum):
    HOME = "http://metis.lti.cs.cmu.edu:4399/"
    MAP = "http://miniserver1875.asuscomm.com:3000/#map=7/42.896/-75.108/"
    REDDIT = "http://metis.lti.cs.cmu.edu:9999/forums/all"
    GITLAB = "http://metis.lti.cs.cmu.edu:8023/explore/"
    SHOPPING = "http://metis.lti.cs.cmu.edu:7770/"


class WebEnvironment:
	def __init__(self):
		self.start_url = None
		self.current_observation = None
		self.env = None

	def observe(self):
		return flatten_axtree_to_str(self.current_observation["axtree_object"])

	def interact(self, action_name, arguments=[]):
		real_action_name = None
		real_arguments = None
		match action_name:
			case "click":
				real_action_name = "click"
				real_arguments = arguments
			case "type":
				real_action_name = "fill"
				real_arguments = arguments[:2]
			case "go_back":
				real_action_name = "go_back"
				real_arguments = []
			case "go_home":
				real_action_name = "goto"
				real_arguments = [self.start_url]
		action = print_gym_call(real_action_name, real_arguments)
		print(f"Just issued action {action}")
		obs, reward, terminated, truncated, info = self.env.step(action)
		if action_name == "type" and int(arguments[-1]) == 1:
			obs, reward, terminated, truncated, info = self.env.step(print_gym_call("press", [arguments[0], "Enter"]))
		self.current_observation = obs



	def load(self, url):
		self.env = gym.make(
		    "browsergym/openended",
		    task_kwargs={"start_url": url},
		    wait_for_user_message=False,
		)
		obs, info = self.env.reset()
		self.current_observation = obs
		self.start_url = url
