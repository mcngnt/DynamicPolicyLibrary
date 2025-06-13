from utils import *
# from enum import Enum
import gymnasium as gym
import browsergym.core
import browsergym.webarena
from browsergym.utils.obs import flatten_axtree_to_str, flatten_dom_to_str, prune_html
from obs_opt import (
    prune_tree,
    translate_node_to_str,
)



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



class WebEnvironment:
	def __init__(self):
		self.start_url = None
		self.current_observation = None
		self.current_url = ""
		self.env = None

		self.webarena_actions_history = []
		self.obs_info_history = []
		self.browserenv_env = None

	def observe(self):
		# print(prune_html(flatten_dom_to_str(self.current_observation["dom_object"])))
		# 1662 with not visible
		# 11999 with all
		# 4259 with only bid
		tr = flatten_axtree_to_str(self.current_observation["axtree_object"], extra_properties={},filter_visible_only=False, filter_with_bid_only=True)
		# print(tr)
		# print(len(tr))
		return tr, self.current_observation["url"], self.current_observation["screenshot"]

	# def observe(self):
	# 	# print(self.current_observation.keys())
	# 	root_node = self.current_observation["axtree_object"]
	# 	print(root_node)
	# 	# print(root_node)
	# 	DOM_root_node = prune_tree(objective="", root_node=root_node, mode="node")
	# 	DOM_str = translate_node_to_str(node=DOM_root_node, mode="concise")
	# 	print(DOM_str)
	# 	return DOM_str, self.current_url, self.current_observation["screenshot"]

	# def observation(self): 
	# 	self.url = self.webarena_env.page.url
	# 	if self.global_config and self.global_config.env.prune:
	# 		root_node = self.obs["text"][1]
	# 		DOM_root_node = prune_tree(objective=self.objective, root_node=root_node, mode="node")
	# 		DOM_str = translate_node_to_str(node=DOM_root_node, mode="concise")
	# 		return {"text": DOM_str, "image": self.obs["image"], "node": DOM_root_node}
	# 	else:
	# 		browser_content = self.obs["text"][0]
	# 		browser_content = browser_content.split("\n")[:self.max_browser_rows] 
	# 		browser_content = "\n".join(browser_content)
	# 		return browser_content


	def interact(self, action_name, arguments=[]):
		gym_action_name = action_name
		gym_arguments = arguments
		match action_name:
			case "click":
				gym_action_name = "click"
				gym_arguments = arguments
			case "type":
				gym_action_name = "fill"
				gym_arguments = arguments[:2]
			case "go_back":
				gym_action_name = "go_back"
				gym_arguments = []
			case "go_home":
				gym_action_name = "goto"
				gym_arguments = [self.start_url]
			case "note":
				return
			case _:
				pass
		action = print_gym_call(gym_action_name, gym_arguments)
		self.webarena_actions_history += [print_action_call(action_name, gym_arguments)]
		print(f"Just issued gym action {action}")
		obs, reward, terminated, truncated, info = self.env.step(action)
		self.obs_info_history += [(obs, info)]
		if action_name == "type" and int(arguments[-1]) == 1:
			self.webarena_actions_history += [print_action_call("press", [arguments[0], "Enter"])]
			obs, reward, terminated, truncated, info = self.env.step(print_gym_call("press", [arguments[0], "Enter"]))
			self.obs_info_history += [(obs, info)]
		self.current_observation = obs
		self.current_url = obs["url"]
		self.browserenv_env = self.env.env.env



	def load(self, task_id):
		self.env = gym.make(f"browsergym/webarena.{task_id}", wait_for_user_message=False)
		obs, info = self.env.reset()
		self.current_observation = obs
		self.start_url = obs["url"]
		self.current_url = obs["url"]
		self.webarena_actions_history = []
		self.obs_info_history = [(obs, info)]
		observation, _, _ = self.observe()
		self.browserenv_env = self.env.env.env
		return obs["goal"], observation
