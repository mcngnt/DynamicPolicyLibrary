import gymnasium as gym
import browsergym.core
from browsergym.webarena import task
import os

from evaluator import evaluate_task

url = "http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/a11yproject/a11yproject.com/-/issues/?sort=created_date&state=opened&first_page_size=20"

task_id = 45

answer = ""


print(evaluate_task(task_id, url, answer))