from utils import *
from policy_library import PolicyLibrary

from prompts.writing_policy import write_policy
from prompts.get_action import get_action
from prompts.critique import get_critique
from prompts.get_policy import get_policy

class Agent:
	def __init__(self, is_exploration,name="default", policy_library_path=None):
		self.exploration_mode = is_exploration
		self.library = PolicyLibrary(path=policy_library_path)
		self.objective = None
		self.trajectory = None
		self.policy_stack = None
		self.name = name
		self.steps_nb = 0

	def load(self, objective):
		self.objective = objective
		self.trajectory = [] 
		self.policy_stack = [{"name":"root", "query":objective, "actions":[]}]
		self.steps_nb = 0

	def get_action(self, observation, url):
		action = {}
		is_final = False
		is_root = len(self.policy_stack) == 1
		top_policy = self.policy_stack[-1]

		policy_objective = print_action_call(top_policy["name"], [top_policy["query"]]) if not is_root else self.objective
		guidance_text = self.library.get(top_policy["name"])[-1] if not is_root else ""

		log_info = {"objective":policy_objective, "observation":None, "guidance":guidance_text,"relevant_policies":None, "action":None, "is_page_op":None, "is_stop":None, "reason":None, "description":None,"critique":None, "plan":None, "created_policies":None}


		if self.steps_nb == 0 and self.exploration_mode:
			relevant_policies = self.library.retrieve(self.objective, k=5)
			policy_feedback = get_policy(self.objective, observation, url, relevant_policies)
			log_info["created_policies"] = policy_feedback["policies"]
			log_info["plan"] = policy_feedback["plan"]
			for policy in policy_feedback["policies"]:
				if self.library.is_new(policy["name"]):
					self.library.update(policy["name"], policy["description"], "")


		relevant_policies = self.library.retrieve(policy_objective, exclude_policy=top_policy["name"])
		log_info["relevant_policies"] = relevant_policies
		action = get_action(policy_objective, observation, url, top_policy["actions"], guidance_text, relevant_policies)
		log_info["action"] = action["call"]
		log_info["reason"] = action["reason"]
		log_info["is_page_op"] = action["is_page_op"]
		log_info["is_stop"] = action["is_stop"]

		top_policy["actions"] += [print_action_call(action["name"], action["arguments"])]
		self.trajectory += [(print_action_call(action["name"], action["arguments"]), observation)]

		is_final = action["is_stop"] and len(self.policy_stack) == 1

		if action["is_stop"] and len(self.policy_stack) > 1:
			prev_policy_name, prev_query, prev_actions = self.policy_stack.pop().values()
			self.policy_stack[-1]["actions"] += [print_action_call("stop", action["arguments"])]
			if self.exploration_mode:
				critique_feedback = get_critique(print_action_call(prev_policy_name, [prev_query]), observation, url, prev_actions)
				log_info["critique"] = critique_feedback["critique"]
				if not int(critique_feedback["perfect"]):
					prev_policy_descr, prev_policy_content = self.library.get(prev_policy_name)
					policy_writing_feedback = write_policy(prev_policy_name, prev_policy_descr, prev_query, prev_actions, critique_feedback["critique"], prev_policy_content)
					self.library.update(prev_policy_name, prev_policy_descr, policy_writing_feedback["guidance"])
		
		if (not action["is_stop"]) and (not action["is_page_op"]): 
			self.policy_stack += [{"name":action["name"], "query":action["arguments"][0], "actions":[]}]
			descr,_ = self.library.get(action["name"])
			log_info["description"] = descr


		self.library.save(f"policies/{self.name}.json")
		self.steps_nb += 1
		return action["name"], action["arguments"], action["is_page_op"], is_final, log_info