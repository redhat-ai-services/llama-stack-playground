# Example Apps

This folder contains a set of example applications.

## Folder Structure

- `agent-chat/` - Apps for talking/testing an Agent.
- `model-chat/` - Apps for talking/testing inference endpoint
- `tools/` - Apps for testing tools

> [!TIP]  
> Llama stack is quickly changing and this repo is designed to allow for rapid testing. These example applications may be works in progress, or out-dated. Try to mark them WIP if it is something that is not tested out.

## How to use

Install Requirements

```sh
pip instal -r requirements
```

Create `.env` file.

> We are using the `dotenv` library which uses a `.env` file. Use the `.env-example` as an example of required environment variables

Run application

```sh
python model-chat/basic-chat-complete-streaming.py
```
