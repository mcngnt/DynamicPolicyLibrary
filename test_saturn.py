from openai import OpenAI
from api_keys import saturn_key

# Initialize the OpenAI client with your API key and base URL
client = OpenAI(
    api_key=saturn_key,
    base_url="https://pd-jerom-llama-33-16406b4644034adb887f0a7595866014.nvidia-oci.saturnenterprise.io/v1"
)

# Send a chat completion request
response = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct",
    messages=[
        {"role": "user", "content": "Hello, world!"}
    ]
)

# Print the model's response
print(response.choices[0].message.content)
