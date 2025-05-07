import json
import os
import re
import subprocess
import time
import sys
from pathlib import Path



def evaluate_task(task_id, actions_history, observation_history, browserenv_env, answer=""):

    original_cwd = os.getcwd()
    webarena_path = Path(__file__).parent / "custom_webarena"
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

    # env = ScriptBrowserEnv(
    #     headless=True,
    #     slow_mo=0,
    #     observation_type="accessibility_tree",
    #     current_viewport_only=True,
    #     viewport_size={"width": 1280, "height": 720},
    # )

    # obs, info = env.reset(options={"config_file": config_file})
    # trajectory: Trajectory = [{"observation": obs, "info": info}]

    # for action in actions_history:
    #     webarena_action = create_id_based_action(action)
    #     trajectory.append(webarena_action)

    #     obs, _, _, _, info = env.step(click_action)

    #     state_info: StateInfo = {"observation": obs, "info": info}
    #     trajectory.append(state_info)

    config_file = f"config_files/{task_id}.json"

    init_obs, init_info = observation_history[0]
    trajectory: Trajectory = [{"observation": init_obs, "info": init_info}]
    for i, action in enumerate(actions_history):
        trajectory.append(create_id_based_action(action))
        obs, info = observation_history[i+1]
        trajectory.append({"observation": obs, "info": info})

    trajectory.append(create_stop_action(answer))

    evaluator = evaluator_router(config_file)
    score = evaluator(
        trajectory=trajectory,
        config_file=config_file,
        page=browserenv_env.page,
        # client=browserenv_env.get_page_client(browserenv_env.page),
        client=None
        # client=browserenv_env.page.client
    )

    os.chdir(original_cwd)

    return score



