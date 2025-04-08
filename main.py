
from web_environment import WebEnvironment, AvailableURL
from agent import Agent

tasks = [
("Tell me the full address of all international airports that are within a driving distance of 30 km to Carnegie Art Museum",
AvailableURL.MAP.value, 9, "Pittsburgh International Airport, Southern Beltway, Findlay Township, Allegheny County, 15231, United States"),
("How many commits did kilian make to a11yproject on 3/1/2023?",
AvailableURL.GITLAB.value, 134, "0"),
("List out reviewers, if exist, who mention about ear cups being small", 
AvailableURL.SHOPPING.value + "6s-wireless-headphones-over-ear-noise-canceling-hi-fi-bass-foldable-stereo-wireless-kid-headsets-earbuds-with-built-in-mic-micro-sd-tf-fm-for-iphone-samsung-ipad-pc-black-gold.html", 
21, "unknown"),
("I have a lot of Nintendo Switch game cards now, help me find the best storage option to fit all 31 cards",
AvailableURL.SHOPPING.value, 159, "Unknown")
]

env = WebEnvironment()
agent = Agent(is_exploration=True)
for (objective, url, _, _) in [tasks[1]]:
    env.load(url)
    agent.load(objective)
    final_answer = None
    # Capping maximum number of prompt iteration
    for i in range(100):
        observation, url = env.observe()
        name, args, is_page_op, is_final = agent.get_action(observation, url)
        if is_page_op:
            env.interact(name, args)
        if is_final:
            final_answer = args[0]
            break    

    print(f"{'-'*10}\nFor the task :\n{objective}\nMy final answer is : {final_answer}\n{'-'*10}\n")


