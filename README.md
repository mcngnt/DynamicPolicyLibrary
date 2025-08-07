# **DynPol**: Dynamic Policies for LLM Web Agents

## Installation

Clone this repo and follow these steps:
- Create a virtual environment if needed (Python 3.10.17 was used for this project)
- Install the required packages:
```bash
pip install -r requirements.txt
```

## Running the architecture

- Set up your backend LLMs (see `generate_content` and `get_embedding` functions in `utils.py`)
- Set up the environment variables:
```bash
./setup_webarena.sh
```
- Run the architecture:
```bash
./run.sh
```
- To change the parameters of the experiments (number of tasks, number of iterations over this set of tasks, etc.), you can edit the `main.py` file (the parameters are located below line 28: `match args.agent_type`)

If you want to change the running architecture, change the `agent_type` parameter for `main.py` inside `run.sh`:
- `dynamic` to run DynPol (default)
- `step` to run the SetP architecture
- `base` to run a single LLM