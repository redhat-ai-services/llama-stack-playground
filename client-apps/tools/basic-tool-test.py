import asyncio
from llama_stack_client import LlamaStackClient
from termcolor import colored

import os
from dotenv import load_dotenv
from llama_stack_client.lib.agents.agent import Agent
from llama_stack_client.types.agent_create_params import AgentConfig
from llama_stack_client.lib.agents.event_logger import EventLogger
load_dotenv()

# if "TAVILY_SEARCH_API_KEY" not in os.environ:
#         print(
#             colored(
#                 """
#                 Error: TAVILY_SEARCH_API_KEY must be set to use this script.
#                 Free API key can be obtained at https://app.tavily.com/
#                 And set using `export TAVILY_SEARCH_API_KEY=<your_api_key>` in your terminal.
#                 """,
#                 "red",
#             )
#         )
#         exit(1)



client = LlamaStackClient(
  base_url=os.environ.get("INFER_URL"),
  # provider_data={"tavily_search_api_key": os.getenv("TAVILY_SEARCH_API_KEY")},
)


# List all tools
all_tools = client.tools.list()
print("All tools:")
for tool in all_tools:
    print(f"- {tool.identifier}")
result = client.tool_runtime.invoke_tool(
    tool_name="web_search", kwargs={"query": "Search the web for the Capitals current win/loss record"}
)
print(result)