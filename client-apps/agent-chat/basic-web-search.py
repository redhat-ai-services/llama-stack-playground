# IMPORTANT: This agent does not work because of the following issue:
# https://github.com/meta-llama/llama-stack/issues/1277

import asyncio
from llama_stack_client import LlamaStackClient
from termcolor import colored

import os
from dotenv import load_dotenv
from llama_stack_client.lib.agents.agent import Agent
from llama_stack_client.types.agent_create_params import AgentConfig
from llama_stack_client.lib.agents.event_logger import EventLogger
load_dotenv()

# NOTE: Due to the following issue we have to use brave search which must be configured in the stack directly
# https://github.com/meta-llama/llama-stack/issues/1277
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
  provider_data={"tavily_search_api_key": os.getenv("TAVILY_SEARCH_API_KEY")},
)

available_shields = [shield.identifier for shield in client.shields.list()]
if not available_shields:
    print(f"No available shields. Disabling safety.")
else:
    print(f"Available shields found: {available_shields}")

agent_config = AgentConfig(
  model=os.environ.get("LLAMA_MODEL"),
  instructions="You are a helpful assistant",
  sampling_params={
    "strategy": {"type": "top_p", "temperature": 1.0, "top_p": 0.9},
  },
  toolgroups=(
    [
      "builtin::websearch",
    ]
  ),
  tool_config={
    "builtin::websearch": {
        "provider_data": {
            "tavily_search_api_key": os.getenv("TAVILY_SEARCH_API_KEY"),
        }
    }
  },
  input_shields=available_shields if available_shields else [],
  output_shields=available_shields if available_shields else [],
  enable_session_persistence=False,
)
agent = Agent(client, agent_config)
user_prompts = [
    "Hello",
    "Search the web for the Capitals current win/loss record",
]

session_id = agent.create_session("test-session")

for prompt in user_prompts:
    response = agent.create_turn(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        session_id=session_id,
    )


    for log in EventLogger().log(response):
        log.print()
