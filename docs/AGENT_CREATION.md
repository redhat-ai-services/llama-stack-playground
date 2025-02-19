# Agent Creation

## Overview

Guide for creating an agent using Curl commands.

## Env Setup

```sh
export LLAMA_STACK_URL=https://xxxx.openshiftapps.com
```

## Basic Agent Creation

  ```sh
  curl -X 'POST' \
    '$LLAMA_STACK_URL/v1/agents' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "agent_config": {
      "sampling_params": {
        "strategy": {
          "type": "greedy"
        },
        "max_tokens": 500,
        "repetition_penalty": 1
      },
      "max_infer_iters": 10,
      "model": "meta-llama/Llama-3.1-8B-Instruct",
      "instructions": "You are a helpful assistant. Answer the user'\''s questions to the best of your ability.",
      "enable_session_persistence": false
    }
  }'
  ```

> Note: Capture the Agent Id returned by this command and store it in the env `AGENT_ID`

## Create Session

In order to interact with our agent we need to create a session associated with it.

```sh
curl -X 'POST' \
  'https://my-llama-stack.openshiftapps.com/v1/agents/$AGENT_ID/session' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "session_name": "test-session"
}'
```

> Note: Capture the session ID stored in this command and save it in `SESSION_ID`

## Validate Agent

```sh
curl -X 'POST' \
  'https://my-llama-stack.openshiftapps.com/v1/agents/$AGENT_ID/session/$SESSION_ID/turn' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "messages": [
    {
      "role": "user",
      "content": "tell me a story"
    }
    
  ],
  "stream": true
}'
  ```
