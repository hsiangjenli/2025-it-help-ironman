import os
from langfuse.openai import OpenAI

os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-xxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
os.environ["LANGFUSE_SECRET_KEY"] = "sk-xxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
os.environ["LANGFUSE_HOST"] = "http://localhost:3000"

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

response = client.chat.completions.create(
    model="gemma3:270m",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who was the first person to step on the moon?"},
        {
            "role": "assistant",
            "content": "Neil Armstrong was the first person to step on the moon on July 20, 1969, during the Apollo 11 mission.",
        },
        {
            "role": "user",
            "content": "What were his first words when he stepped on the moon?",
        },
    ],
)

print(response.choices[0].message.content)
