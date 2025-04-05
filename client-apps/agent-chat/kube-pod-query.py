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


client = LlamaStackClient(
  base_url=os.environ.get("INFER_URL"),
)

available_shields = [shield.identifier for shield in client.shields.list()]
if not available_shields:
    print(f"No available shields. Disabling safety.")
else:
    print(f"Available shields found: {available_shields}")

agent_config = AgentConfig(
  model=os.environ.get("LLAMA_MODEL"),
  instructions="You are an expert Kubernetes assistant. You can help users manage their Kubernetes clusters by providing information about pods, services, and other resources. Namespace will always be assumed to be llama-stack-agent",
  sampling_params={
    "strategy": {"type": "top_p", "temperature": 1.0, "top_p": 0.9},
    "max_tokens": 512,  # Set a maximum token limit for the response
  },
  toolgroups=(
    [
      "mcp::kube-service",
    ]
  ),
  input_shields=available_shields if available_shields else [],
  output_shields=available_shields if available_shields else [],
  enable_session_persistence=False,
)
agent = Agent(client, agent_config)
user_prompts = [
    "Create a new Kubernetes pod named 'nginx-pod' in the 'llama-stack-agent' namespace with the nginx image and expose it on port 80",
    "Give a list of pods"
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
