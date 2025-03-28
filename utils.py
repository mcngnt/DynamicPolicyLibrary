from google import genai
import numpy as np
import re

# client = genai.Client(api_key="***REMOVED***")
client = genai.Client(api_key="***REMOVED***")


def generate_content(prompt):
    response = client.models.generate_content(
    model="gemini-2.0-flash", contents=prompt
    )
    return response.text

def get_embedding(prompt):
    result = client.models.embed_content(
        model="text-embedding-004",
        contents=prompt
    )
    return np.asarray(result.embeddings[0].values)

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