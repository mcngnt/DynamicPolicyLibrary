from utils import *
from policy_library import PolicyLibrary

from prompts.step import get_action


class StepAgent:
	def __init__(self,name="default", policy_library_path=None):
		self.library = PolicyLibrary(path=policy_library_path)
		self.objective = None
		self.trajectory = None
		self.policy_stack = None
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

		policy_objective = print_action_call(top_policy["name"], [top_policy["query"]]) if not is_root else self.objective
		guidance_text = self.library.get(top_policy["name"])[1] if not is_root else ""
		# policy_description = self.library.get(top_policy["name"])[0] if not is_root else ""

		log_info = {"objective":policy_objective, "observation":observation,"url":url, "steps_nb":self.steps_nb, "guidance":guidance_text,"relevant_policies":None, "action":None, "is_page_op":None, "is_stop":None, "reason":None, "description":None,"critique":None, "plan":None, "created_policies":None, "end_screenshot":None}

		
		action = get_action(policy_objective, observation, url, top_policy["actions"], guidance_text)

		print(f"get_action feedback : {action}\n")
		log_info["action"] = action["call"]
		log_info["reason"] = action["reason"]
		log_info["is_page_op"] = action["is_page_op"]
		log_info["is_stop"] = action["is_stop"]

		top_policy["actions"] += [print_action_call(action["name"], action["arguments"])]
		self.trajectory += [(print_action_call(action["name"], action["arguments"]), observation)]

		is_final = action["is_stop"] and len(self.policy_stack) == 1

		if action["is_stop"] and len(self.policy_stack) > 1:
			prev_policy_name, prev_query, prev_actions, prev_inital_observation = self.policy_stack.pop().values()
			policy_call = self.policy_stack[-1]["actions"][-1]
			self.policy_stack[-1]["actions"][-1] = f"{action['arguments'][0]} = {policy_call}"
		
		if (not action["is_stop"]) and (not action["is_page_op"]): 
			self.policy_stack += [{"name":action["name"], "query":action["arguments"][0], "actions":[], "inital_observation":observation}]
			descr,_ = self.library.get(action["name"])
			log_info["description"] = descr

		if is_final:
			log_info["end_screenshot"] = screenshot


		self.steps_nb += 1
		return action["name"], action["arguments"], action["is_page_op"], is_final, log_info