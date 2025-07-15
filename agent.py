from utils import *
from policy_library import PolicyLibrary

from prompts.writing_policy import write_policy
from prompts.get_action import get_action
from prompts.critique import get_critique
from prompts.get_policy import get_policy

class Agent:
	def __init__(self,name="default", policy_library_path=None, only_policy=False, generate_new_policies=True, improve_policies=True, default_policy_library_path="policies/step_policies.json"):
		self.library = PolicyLibrary(path=policy_library_path, default_path=default_policy_library_path)
		self.objective = None
		self.trajectory = None
		self.policy_stack = None
		self.name = name
		self.steps_nb = 0
		self.site = None
		self.only_policy = only_policy
		self.generate_new_policies =  generate_new_policies
		self.improve_policies = improve_policies
		self.current_plan = ""

	def load(self, objective, observation, site):
		self.objective = objective
		self.trajectory = [] 
		self.policy_stack = [{"name":"root", "query":objective, "actions":[], "inital_observation":observation}]
		self.steps_nb = 0
		self.site = site
		self.current_plan = ""


	def get_action(self, observation, url, screenshot):
		action = {}
		is_final = False
		is_root = len(self.policy_stack) == 1
		top_policy = self.policy_stack[-1]

		print(f'Here are the current actions performed in the {print_action_call(top_policy["name"], [top_policy["query"]])} subroutine : {top_policy["actions"]}\n')

		policy_objective = print_action_call(top_policy["name"], [top_policy["query"]]) if not is_root else self.objective
		guidance_text = self.library.get(top_policy["name"])[1] if not is_root else ""
		policy_description = self.library.get(top_policy["name"])[0] if not is_root else ""

		log_info = {"objective":policy_objective, "observation":observation,"url":url, "steps_nb":self.steps_nb, "guidance":guidance_text,"relevant_policies":None, "action":None, "is_page_op":None, "is_stop":None, "reason":None, "description":None,"feedback":None,"success":None, "plan":None, "created_policies":None, "end_screenshot":None}


		if self.steps_nb == 0 and self.generate_new_policies:
			relevant_policies = self.library.retrieve(self.objective, site=self.site, k=20)
			policy_feedback = get_policy(self.objective, observation, url, relevant_policies)
			print(f"get_policy feedback : {policy_feedback}\n")
			log_info["created_policies"] = policy_feedback["policies"]
			log_info["plan"] = policy_feedback["plan"]
			self.current_plan = policy_feedback["plan"]
			for policy in policy_feedback["policies"]:
				if self.library.is_new(policy["name"]):
					self.library.update(policy["name"], policy["description"], "", self.site)

		if self.only_policy:
			return "stop", ["Only creating policies"], False, True, log_info

		
		relevant_policies = self.library.retrieve(policy_objective, exclude_policy=top_policy["name"], site=self.site,k=10)
		log_info["relevant_policies"] = relevant_policies
		if len(top_policy["actions"]) > 15:
			action = {"name":"stop", "arguments":["Task not achieved : too many steps."], "is_page_op":False,"is_stop":True, "reason":"This action was taken automatically beacause of the high number of steps of the policy.", "call":"stop [ask not achieved : too many steps.]"}
		else:
			action = get_action(policy_objective, policy_description, observation, url, top_policy["actions"], guidance_text, relevant_policies, is_root, self.current_plan, step_nb=self.steps_nb)
		print(f"get_action feedback : {action}\n")
		log_info["action"] = action["call"]
		log_info["reason"] = action["reason"]
		log_info["is_page_op"] = action["is_page_op"]
		log_info["is_stop"] = action["is_stop"]

		top_policy["actions"] += [(print_action_call(action["name"], action["arguments"]), action["reason"])]
		self.trajectory += [(print_action_call(action["name"], action["arguments"]), observation)]

		is_final = action["is_stop"] and len(self.policy_stack) == 1

		if action["is_stop"] and len(self.policy_stack) > 1:
			prev_policy_name, prev_query, prev_actions, prev_inital_observation = self.policy_stack.pop().values()
			self.policy_stack[-1]["actions"] += [(print_action_call("stop", action["arguments"]), action["reason"])]
			if self.improve_policies:
				critique_feedback = get_critique(print_action_call(prev_policy_name, [prev_query]), observation, url, prev_actions, prev_inital_observation)
				print(f"get_critique feedback : {critique_feedback}\n")
				log_info["feedback"] = critique_feedback["feedback"]
				nb_used, nb_failed = self.library.report_use(prev_policy_name, int('1' in critique_feedback["success"]))
				if nb_used == nb_failed and nb_used >= 3:
					self.library.reset(prev_policy_name)
				else:
					if (nb_used == 1) or (float(nb_failed)/float(nb_used) > 0.5):
						prev_policy_descr, prev_policy_content = self.library.get(prev_policy_name)
						policy_writing_feedback = write_policy(prev_policy_name, prev_policy_descr, prev_query, observation, critique_feedback["breakdown"], critique_feedback["feedback"], prev_policy_content, prev_inital_observation)
						print(f"write_policy feedback : {policy_writing_feedback}\n")
						self.library.update(prev_policy_name, prev_policy_descr, policy_writing_feedback["guidance"], self.site)
		
		if (not action["is_stop"]) and (not action["is_page_op"]): 
			self.policy_stack += [{"name":action["name"], "query":action["arguments"][0], "actions":[], "inital_observation":observation}]
			descr,_ = self.library.get(action["name"])
			log_info["description"] = descr


		log_info["end_screenshot"] = screenshot


		self.steps_nb += 1
		return action["name"], action["arguments"], action["is_page_op"], is_final, log_info