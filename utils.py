from google import genai
import numpy as np
import re

api_keys = [
"***REMOVED***",
"***REMOVED***",
"***REMOVED***",
"***REMOVED***",
]

current_key_id = 0

client = genai.Client(api_key=api_keys[0])

def switch_api_key():
    global current_key_id, client
    print("Switching API key.")
    current_key_id += 1
    client = genai.Client(api_key=api_keys[current_key_id % len(api_keys)])


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
    call = re.sub(r'\s*\[', '[', call)
    match = re.match(r'([a-zA-Z_][a-zA-Z0-9_]*)(\[(.*?)\])?(.*)', call)
    return [match.group(1)] + ([match.group(3)] if match.group(3) else []) + re.findall(r'\[(.*?)\]', match.group(4)) if match else []