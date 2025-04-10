import json
import os

def build_trace_from_actions(actions):

# "objective":, "observation":, "guidance":,"relevant_policies":, "action":, "is_page_op":, "reason":, "description":, "plan":, "created_policies":}
    root_trace = {"trace": []}
    policy_stack = [root_trace]
    gloabl_plan = None
    global_created_policies = None

    for action in actions:

        if action["plan"]:
            gloabl_plan = action["plan"]
        if action["created_policies"]:
            global_created_policies = action["created_policies"]

        base = {
            "objective" : action["objective"],
            "action" : action["action"],
            "steps_nb" : action["steps_nb"],
            "reason": action["reason"],
            "observation": action["observation"],
            "url" : action["url"],
            "guidance" : action["guidance"],
            "relevant_policies": action["relevant_policies"]
        }

        if action["is_page_op"]:
            op = {
                "type": "page_op",
            } | base
            policy_stack[-1]["trace"].append(op)
        else:
            if not action["is_stop"]:
                policy_entry = {
                    "type": "policy",
                    "description" : action["description"],
                } | base | {"trace": []}
                policy_stack[-1]["trace"].append(policy_entry)
                policy_stack.append(policy_entry)

        if action["is_stop"]:
            stop = {
                "type": "stop",
            } | base
            policy_stack[-1]["trace"].append(stop)
            policy_entry = policy_stack.pop()
            policy_entry["critique"] = action["critique"]
            

    return {
        "created_policies": global_created_policies,
        "plan": gloabl_plan,
        "trace": root_trace
    }


def dump_log(actions, name="log"):
    log = build_trace_from_actions(actions)
    os.makedirs(os.path.dirname(name), exist_ok=True)
    with open(f"{name}.json", "w") as f:
        json.dump(log, f, indent="\t")
    return log
