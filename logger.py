import json

def build_trace_from_actions(actions):

# "objective":, "observation":, "guidance":,"relevant_policies":, "action":, "is_page_op":, "reason":, "description":, "plan":, "created_policies":}
    root_trace = {"trace": []}
    policy_stack = [root_trace]
    global_created_policies = None
    gloabl_plan = None

    for action in actions:
        call = action["action"]
        description = action["description"]
        is_page_op = action["is_page_op"]
        is_stop = action["is_stop"]
        objective = action["objective"]
        observation = action["observation"]
        guidance = action["guidance"]
        relevant_policies = action["relevant_policies"]
        reason = action["reason"]
        plan = action["plan"]
        created_policies = action["created_policies"]
        critique = action["critique"]

        if plan:
            gloabl_plan = plan
        if created_policies:
            global_created_policies = created_policies

        if is_page_op:
            op = {
                "type": "page_op",
                "observation": observation,
                "objective" : objective,
                "guidance" : guidance,
                "action" : call,
                "reason": reason,
                "relevant_policies": relevant_policies
            }
            policy_stack[-1]["trace"].append(op)
        else:
            if not is_stop:
                policy_entry = {
                    "type": "policy",
                    "observation": observation,
                    "objective" : objective,
                    "guidance" : guidance,
                    "action" : call,
                    "reason": reason,
                    "relevant_policies": relevant_policies,
                    "description" : description,
                    "trace": []
                }
                policy_stack[-1]["trace"].append(policy_entry)
                policy_stack.append(policy_entry)

        if is_stop:
            stop = {
                "type": "stop",
                "observation": observation,
                "objective" : objective,
                "guidance" : guidance,
                "action" : call,
                "reason": reason,
            }
            policy_stack[-1]["trace"].append(stop)
            policy_entry = policy_stack.pop()
            policy_entry["critique"] = critique
            

    return {
        "created_policies": global_created_policies,
        "plan": gloabl_plan,
        "trace": root_trace
    }


def dump_log(actions, name="log"):
    log = build_trace_from_actions(actions)
    with open(f"{name}.json", "w") as f:
        json.dump(log, f, indent="\t")
    return log
