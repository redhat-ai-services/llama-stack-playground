from llama_stack_client import LlamaStackClient
from llama_stack_client.types import UserMessage
import os
from dotenv import load_dotenv

load_dotenv()

client = LlamaStackClient(
    base_url=os.environ.get("INFER_URL"),
)

response = client.inference.chat_completion(
    messages=[
        UserMessage(
            content="hello world, write me a 2 sentence poem about the moon",
            role="user",
        ),
    ],
    model_id=os.environ.get("LLAMA_MODEL"),
    stream=False,
)
print(response)