import gymnasium as gym
import browsergym.core
from browsergym.utils.obs import flatten_axtree_to_str, flatten_dom_to_str, prune_html
from browsergym.core.action.highlevel import HighLevelActionSet


# class AvailableURL(Enum):
#     HOME = "http://metis.lti.cs.cmu.edu:4399/"
#     MAP = "http://miniserver1875.asuscomm.com:3000/#map=7/42.896/-75.108"
#     REDDIT = "http://metis.lti.cs.cmu.edu:9999/forums/all"
#     GITLAB = "http://metis.lti.cs.cmu.edu:8023/explore"
#     SHOPPING = "http://metis.lti.cs.cmu.edu:7770/"

env = gym.make(
    "browsergym/openended",
    task_kwargs={"start_url": "http://ec2-3-140-166-134.us-east-2.compute.amazonaws.com:9999/"},  # starting URL
    wait_for_user_message=False,  # wait for a user message after each agent message sent to the chat
)


obs, info = env.reset()

print(flatten_axtree_to_str(obs["axtree_object"]))

# action_set = HighLevelActionSet(
#             subsets=["chat", "tab", "nav", "bid", "infeas"],  # define a subset of the action space
#             # subsets=["chat", "bid", "coord", "infeas"] # allow the agent to also use x,y coordinates
#             strict=False,  # less strict on the parsing of the actions
#             multiaction=False,  # does not enable the agent to take multiple actions at once
# )



# print(action_set.describe(with_long_description=False, with_examples=True))

action = "click('42')"

obs, reward, terminated, truncated, info = env.step(action)

print(flatten_axtree_to_str(obs["axtree_object"]))


# while True:
#     action = ...  # implement your agent here
#     obs, reward, terminated, truncated, info = env.step(action)
#     if terminated or truncated:
#         break
# release the environment


env.close()