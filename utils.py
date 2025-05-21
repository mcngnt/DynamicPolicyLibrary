from google import genai
from openai import OpenAI
import numpy as np
import re
import json
import os

from api_keys import gemini_keys, saturn_key, saturn_url


current_key_id_gemini = 0
gemini_client = genai.Client(api_key=gemini_keys[0])

def switch_api_key_gemini():
    global current_key_id_gemini, gemini_client
    print("Switching Gemini API key.")
    current_key_id_gemini += 1
    gemini_client = genai.Client(api_key=gemini_keys[current_key_id_gemini % len(gemini_keys)])


def generate_content_gemini(prompt):
    try:
        response = gemini_client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
        )
        return response.text
    except Exception as e:
        print("Error in generating content :", e)
        switch_api_key_gemini()
        return generate_content_gemini(prompt)



saturn_client = OpenAI(
    api_key=saturn_key,
    base_url=saturn_url
)


def generate_content_saturn(prompt):
    response = saturn_client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


def generate_content(prompt):
    return generate_content_gemini(prompt)
    # return generate_content_saturn(prompt)


def get_embedding_gemini(prompt):

    try:
        result = gemini_client.models.embed_content(
        model="text-embedding-004",
        contents=prompt
        )
        return np.asarray(result.embeddings[0].values)
    except:
        switch_api_key_gemini()
        return get_embedding_gemini(prompt)



def get_embedding(prompt):
    return get_embedding_gemini(prompt)


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


def get_site_type(task_id):
    config_file = f"custom_webarena/config_files/{task_id}.json"
    try:
        with open(config_file, 'r') as file:
            data = json.load(file)
    except:
        if os.path.exists(config_file):
            return get_site_type(task_id)

    sites = data.get('sites', [])
    if "wikipedia" in sites:
        sites.remove("wikipedia")
    return sites[0]


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