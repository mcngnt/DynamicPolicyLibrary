import json
import os
import re
import subprocess
import time
import sys
from pathlib import Path



def evaluate_task(task_id, url, answer=""):

    original_cwd = os.getcwd()
    webarena_path = Path(__file__).parent / "webarena"
    os.chdir(webarena_path)
    sys.path.insert(0, str(webarena_path))


    from browser_env import (
        Action,
        ActionTypes,
        ObservationMetadata,
        ScriptBrowserEnv,
        StateInfo,
        Trajectory,
        action2str,
        create_id_based_action,
        create_stop_action,
    )
    from evaluation_harness.evaluators import evaluator_router

    env = ScriptBrowserEnv(
        headless=True,
        slow_mo=0,
        observation_type="accessibility_tree",
        current_viewport_only=True,
        viewport_size={"width": 1280, "height": 720},
    )

    config_file = f"config_files/{task_id}.json"
    eval_config_file = f"config_files/eval_{task_id}.json"


    with open(config_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    data["start_url"] = url

    with open(eval_config_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    trajectory: Trajectory = []


    obs, info = env.reset(options={"config_file": eval_config_file})
    actree_obs = obs["text"]

    state_info: StateInfo = {"observation": obs, "info": info}
    trajectory.append(state_info)

    trajectory.append(create_stop_action(answer))


    evaluator = evaluator_router(eval_config_file)
    score = evaluator(
        trajectory=trajectory,
        config_file=eval_config_file,
        page=env.page,
        client=env.get_page_client(env.page),
    )

    os.chdir(original_cwd)

    return score



