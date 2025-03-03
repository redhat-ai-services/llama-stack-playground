# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.
import os
from typing import Optional

import fire
from llama_stack_client import LlamaStackClient
from llama_stack_client.lib.agents.agent import Agent
from llama_stack_client.lib.agents.event_logger import EventLogger
from llama_stack_client.types.agent_create_params import AgentConfig
from termcolor import colored
from llama_stack_client.lib.agents.event_logger import EventLogger
from dotenv import load_dotenv



def main(model_id: Optional[str] = None):
    load_dotenv()
    if "TAVILY_SEARCH_API_KEY" not in os.environ:
        print(
            colored(
                "Warning: TAVILY_SEARCH_API_KEY is not set; will not use websearch tool.",
                "yellow",
            )
        )

    client = LlamaStackClient(
        base_url=os.environ.get('INFER_URL'),
        provider_data={"tavily_search_api_key": os.getenv("TAVILY_SEARCH_API_KEY")},
    )

    available_shields = [shield.identifier for shield in client.shields.list()]
    if not available_shields:
        print(colored("No available shields. Disabling safety.", "yellow"))
    else:
        print(f"Available shields found: {available_shields}")

    llm_inference_provider_ids = [
        p.provider_id
        for p in client.providers.list()
        if p.api == "inference" and p.provider_type != "sentence-transformers"
    ]

    if model_id is not None:
        client.models.register(
            model_id=model_id,
            model_type="llm",  # model_type
            provider_id=llm_inference_provider_ids[0],
            provider_model_id=model_id,
        )

    available_models = [
        model.identifier
        for model in client.models.list()
        if model.model_type == "llm" and "405B" not in model.identifier
    ]
    if not available_models:
        print(colored("No available models. Exiting.", "red"))
        return
    elif model_id is not None:
        selected_model = model_id
    else:
        selected_model = available_models[0]
        print(f"Using model: {selected_model}")

    agent_config = AgentConfig(
        model=selected_model,
        instructions="You are a helpful assistant",
        sampling_params={
            "strategy": {"type": "top_p", "temperature": 1.0, "top_p": 0.9},
        },
        toolgroups=(
            [
                "builtin::websearch",
            ]
            if os.getenv("TAVILY_SEARCH_API_KEY")
            else []
        ),
        input_shields=available_shields if available_shields else [],
        output_shields=available_shields if available_shields else [],
        enable_session_persistence=False,
    )
    agent = Agent(client, agent_config)
    user_prompts = [
        # "Hello",
        "Search web for which players played in the winning team of the NBA western conference semifinals of 2024",
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


if __name__ == "__main__":
    fire.Fire(main)