# Llama Stack Local Setup

Info for setting up Llama Stack Locally

## Run Llama Stack Using Podman

The simpiliest wy in which to use the Llama Stack locally is to set it up using Podman and point to an existing model in vLLM

> [!NOTE]  
> The llama stack is currently only able to interact directly with Llama Models

### Run With Default Template

Set Env Vars:

```sh
export VLLM_URL=https://<MY_VLLM_URL>:443/v1
export VLLM_API_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxx
export INFERENCE_MODEL=meta-llama/Llama-3.1-8B-Instruct
export LLAMA_STACK_PORT=5001
# Only Required for Custom Template
export RUN_FILE=custom-run.yaml
```

```sh
podman \
 run \
  -it \
  -p $LLAMA_STACK_PORT:$LLAMA_STACK_PORT \
  llamastack/distribution-remote-vllm \
  --port $LLAMA_STACK_PORT \
  --env INFERENCE_MODEL=$INFERENCE_MODEL \
  --env VLLM_URL=$VLLM_URL \
  --env VLLM_API_TOKEN=$VLLM_API_TOKEN
```

### Run With Custom Template

```sh
podman \
 run \
  -it \
  -p $LLAMA_STACK_PORT:$LLAMA_STACK_PORT \
  -v $RUN_FILE:/config/run.yaml:z \
  llamastack/distribution-remote-vllm \
  --yaml-config /config/run.yaml \
  --port $LLAMA_STACK_PORT \
  --env INFERENCE_MODEL=$INFERENCE_MODEL \
  --env VLLM_URL=$VLLM_URL \
  --env VLLM_API_TOKEN=$VLLM_API_TOKEN
```

## Basic Server Test

```sh
curl --request POST \
  --url http://localhost:5001/v1/inference/chat-completion \
  --header 'Accept: application/json, text/event-stream' \
  --header 'Content-Type: application/json' \
  --data '{
  "model_id": "meta-llama/Llama-3.1-8B-Instruct",
  "messages": [
    {
      "role": "user",
      "content": "How do I cook an egg?"
    }
  ],
  "stream": true,
  "sampling_params": {
    "strategy": {
      "type": "greedy"
    },
    "max_tokens": 30,
    "repetition_penalty": 1
  }
}'
```

## Installing Llama Stack Locally

> [!NOTE]  
> Note not required for anything else in this README but useful to have.

Install `uv`

`uv pip install llama-stack`

> [!TIP]  
> This creates a bunch of templates inside `/usr/local/lib/python3.13/site-packages/llama_stack/templates/` that can be used.

**Open API Reference:**

https://llama-stack.readthedocs.io/en/latest/references/api_reference/index.html
