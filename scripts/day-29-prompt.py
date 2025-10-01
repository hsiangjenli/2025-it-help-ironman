import os
from langfuse import Langfuse

os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-xxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
os.environ["LANGFUSE_SECRET_KEY"] = "sk-xxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
os.environ["LANGFUSE_HOST"] = "http://localhost:3000"

langfuse = Langfuse()

prompt = langfuse.get_prompt("TEST-PROMPT", label="latest")

print("Prompt: \n", prompt.prompt)
print("=" * 20)
print("Variables: \n", prompt.variables)
print("=" * 20)
print(
    "Compiled: \n",
    prompt.compile(project_name="Langfuse", project_description="Langfuse Description"),
)
