import gymnasium as gym
import browsergym.core
from browsergym.utils.obs import flatten_axtree_to_str, flatten_dom_to_str, prune_html
from browsergym.core.action.highlevel import HighLevelActionSet
from enum import Enum


base_actions = """
Page Operation Actions:
- click [ id ]: To click on an element with its numerical ID on the webpage. E.g. , ‘click [7] ’ If clicking on a specific element doesn ’ t trigger the transition to your desired web state , this is due to the element’s lack of interactivity or GUI visibility . In such cases, move on to interact with OTHER similar or relevant elements INSTEAD.
- type [ id ] [ content ] [ press enter after =0|1]: To type content into a field with a specific ID. By default , the ‘ Enter ’ key is pressed after typing unless ‘press enter after ’ is set to 0. E.g. , ‘type [15] [Carnegie Mellon University ] [1] ’ If you can ’ t find what you’re looking for on your first attempt , consider refining your search keywords by breaking them down or trying related terms.
- go_back : To return to the previously viewed page.
- note [ content ]: To take note of all important info w.r.t. completing the task to enable reviewing it later . E.g. , ‘note [Spent $10 on 4/1/2024] ’
- stop [ answer ]: To stop interaction and return response. Present your answer within the brackets . If the task doesn’t require a textual answer or appears insurmountable, indicate ‘N/A’ and additional reasons and all relevant information you gather as the answer . E.g. , ‘stop [5h 47min]’
- go_home: To return to the homepage where you can find other websites.
"""


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




class AvailableURL(Enum):
    HOME = "http://metis.lti.cs.cmu.edu:4399/"
    MAP = "http://miniserver1875.asuscomm.com:3000/#map=7/42.896/-75.108"
    REDDIT = "http://metis.lti.cs.cmu.edu:9999/forums/all"
    GITLAB = "http://metis.lti.cs.cmu.edu:8023/explore"
    SHOPPING = "http://metis.lti.cs.cmu.edu:7770/"



env = gym.make(
    "browsergym/openended",
    task_kwargs={"start_url": AvailableURL.REDDIT.value},  # starting URL
    wait_for_user_message=False,  # wait for a user message after each agent message sent to the chat
)


obs, info = env.reset()

# print(flatten_axtree_to_str(obs["axtree_object"]))

action_set = HighLevelActionSet(
            subsets=["chat", "tab", "nav", "bid", "infeas"],  # define a subset of the action space
            # subsets=["chat", "bid", "coord", "infeas"] # allow the agent to also use x,y coordinates
            strict=False,  # less strict on the parsing of the actions
            multiaction=False,  # does not enable the agent to take multiple actions at once
)



print(action_set.describe(with_long_description=False, with_examples=True))

action = "click('42')"

obs, reward, terminated, truncated, info = env.step(action)

# print(flatten_axtree_to_str(obs["axtree_object"]))


# while True:
#     action = ...  # implement your agent here
#     obs, reward, terminated, truncated, info = env.step(action)
#     if terminated or truncated:
#         break
# release the environment


env.close()