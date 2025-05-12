from google import genai
import numpy as np
import re
from api_keys import gemini_keys


current_key_id = 0

client = genai.Client(api_key=gemini_keys[0])

def switch_api_key():
    global current_key_id, client
    print("Switching API key.")
    current_key_id += 1
    client = genai.Client(api_key=gemini_keys[current_key_id % len(gemini_keys)])


def generate_content(prompt):
    try:
        response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
        )
        return response.text
    except Exception as e:
        print("Error in generating content :", e)
        switch_api_key()
        return generate_content(prompt)

def get_embedding(prompt):

    try:
        result = client.models.embed_content(
        model="text-embedding-004",
        contents=prompt
        )
        return np.asarray(result.embeddings[0].values)
    except:
        switch_api_key()
        return get_embedding(prompt)


def parse_elements(text, key_list):
        element_dict = {}
        for k in key_list:
            _match = re.search(
                rf"{k.upper()}:\s*(.*?)\s*(?=\n[A-Z\s]*:|$)", text, re.DOTALL
            )
            element_dict[k] = _match.group(1).strip() if _match else ""
        return element_dict

def print_action_call(name, arguments):
    return name + " " + " ".join([f"[{arg}]" for arg in arguments])

def parse_action_call(call):
    pattern = r'(\w+)|\[((?:[^\[\]]+|\[[^\[\]]*\])*)\]'
    
    matches = re.findall(pattern, call)
    result = []

    for match in matches:
        if match[0]:  # function name or bare word
            result.append(match[0])
        else:
            result.append(match[1])
    
    return result

def print_gym_call(name, arguments):
    return f"""{name}({','.join([f"'{arg}'" for arg in arguments])})"""


def step_dict_to_prompt(prompt_dict):
    prompt = prompt_dict["instruction"]
    prompt += "\nHere are a few examples:"

    for example in prompt_dict["examples"]:
            prompt += f"\n### Input:\n{example['input']}\n\n### Response:\n{example['response']}"

    prompt += """Please issue only a single action at a time.
    Adhere strictly to the following output format :
    RESPONSE FORMAT :
    REASON: ...
    ACTION: ...
    """
    prompt += prompt_dict["input"]

    return prompt