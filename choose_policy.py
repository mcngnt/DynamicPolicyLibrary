from utils import *


choose_policy_system_prompt = """
You are a seasoned web navigator. You have to assess the relevance of web-related subroutines compared to a textual descripttion.

You will be provided with the following :
SUBROUTINE CALL:
The subroutine call in the format subroutine [query] like find_customer_review [Show me customer reviews for Antonia Racer Tank]
SUBROUTINE DESCRIPTION:
The subroutine description
AVAILABLE SUBROUTINES:
List of all available subroutines as well as their description

Compare every available subroutine to the subroutine description. See if you can replace the SUBROUTINE CALL by a call to one of the available subroutines so that the two affect the web environment in the same way.

You need to answer in the following format.
COMPARISON:
List every available subroutine and describe how they compared to the proposed subroutine.
ANSWER:
Tell if one of the available subroutines could replace the proposed subroutines, even if you have to change the query.
NEW:
Answer 0 if you could find a fitting subrourine among the available one and 1 if you can't
CALL:
Write down the subroutine call in the format subroutine_name [query].
"""




def choose_policy(policy_name, policy_args, policy_description, available_policies):
    choose_policy_prompt = f"""
    {choose_policy_system_prompt}
    SUBROUTINE CALL: {print_action_call(policy_name, policy_args)}
    SUBROUTINE DESCRIPTION : {policy_description}
    AVAILABLE SUBROUTINES : {[f"{name} [query] : {description}" for (name, description) in available_policies]}
    """

    answer = generate_content(choose_policy_prompt)

    result = parse_elements(answer, ["comparison", "answer", "new", "call"])

    # print("-------")
    # print(result["call"])
    # print("-----")
    
    arguments = parse_action_call(result["call"])

    choose_policy_feedback = {"comparison":result["comparison"], "answer":result["answer"], "new":result["new"], "name":arguments[0], "arguments":arguments[1:]}

    return choose_policy_feedback



# ==== Prompt testing ===


my_policy_name = """search"""

my_policy_args = ["""Carnegie Art Museum"""]


my_policy_description = """This action uses the search bar to find a specific location."""

my_available_policies = [("search_nearest_place", "This Maps subroutine finds places near a given location."), ("find_directions", "This Maps subroutine finds directions between two locations to answer the query.")]


def choose_my_policy():
	return choose_policy(my_policy_name, my_policy_args, my_policy_description, my_available_policies)