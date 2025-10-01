from openai import OpenAI

client = OpenAI(
    api_key="pass",
    base_url="http://localhost:11434/v1",
)

response = client.chat.completions.create(
    model="gemma3:270m",
    messages=[
        {"role": "system", "content": "你是一位臺灣人，請用繁體中文回答。"},
        {"role": "user", "content": "你相信有外星人嗎？"},
    ],
)
print(response.choices[0].message.content)
