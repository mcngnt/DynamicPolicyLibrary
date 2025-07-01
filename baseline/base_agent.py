from utils import *

from prompts.base import get_action


class BaseAgent:
	def __init__(self,name="default"):
		self.objective = None
		self.trajectory = None
		self.name = name
		self.steps_nb = 0
		self.site = None

	def load(self, objective, observation, site):
		self.objective = objective
		self.trajectory = [] 
		self.policy_stack = [{"name":"root", "query":objective, "actions":[], "inital_observation":observation}]
		self.steps_nb = 0
		self.site = site

	def get_action(self, observation, url, screenshot):
		action = {}
		is_final = False
		is_root = len(self.policy_stack) == 1
		top_policy = self.policy_stack[-1]

		print(f'Here are the current actions performed in the {print_action_call(top_policy["name"], [top_policy["query"]])} subroutine : {top_policy["actions"]}\n')

		log_info = {"objective":self.objective, "observation":observation,"url":url, "steps_nb":self.steps_nb, "guidance":"","relevant_policies":None, "action":None, "is_page_op":None, "is_stop":None, "reason":None, "description":None,"feedback":None,"success":None, "plan":None, "created_policies":None, "end_screenshot":None}
		
		action = get_action(self.objective, observation, url, top_policy["actions"])

		print(f"get_action feedback : {action}\n")
		log_info["action"] = action["call"]
		log_info["reason"] = action["reason"]
		log_info["is_page_op"] = action["is_page_op"]
		log_info["is_stop"] = action["is_stop"]

		top_policy["actions"] += [print_action_call(action["name"], action["arguments"])]
		self.trajectory += [(print_action_call(action["name"], action["arguments"]), observation)]

		is_final = action["is_stop"] and len(self.policy_stack) == 1

		if is_final:
			log_info["end_screenshot"] = screenshot

		self.steps_nb += 1
		return action["name"], action["arguments"], action["is_page_op"], is_final, log_info