from llama_stack_client import LlamaStackClientError
import os
from dotenv import load_dotenv

load_dotenv()

client = LlamaStackClient(
    base_url=os.environ.get("INFER_URL")
)

response = client.models.list()
print(response)