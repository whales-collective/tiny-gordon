# 🐢 Tiny Gordon

Tiny Gordon is an AI agent built in a flash using Docker Model Runner, Docker Compose, Google's ADK, and the MCP Toolkit to give it superpowers. This agent is designed to help you master Docker with ease.

> 🚧 this is a work in progress

## Requirements

- Docker Desktop + MCP Toolkit extension
- Install the Brave MCP server (you need an API key - there is a free plan: https://brave.com/search/api/)
- Install the Fetch MCP server - *[optional]*

## Start all the Tiny Gordon Agent

If you are on macOS
```bash
docker compose up --build
```

If you are on Linux:
```bash
docker compose --file compose.linux.yml up --build
```
> - You can change of model by updating the `.env` file
> - ✋ This demo is using tools, so my advice is to stay with `ai/qwen2.5:latest`

🐙 Docker Compose will start **2 services**:
- [http://localhost:8000](http://localhost:8000) to interact with **Tiny Gordon** using a web UI.
- [http://localhost:9000/](http://localhost:9000/) to interact with **Tiny Gordon** using a REST API.

## Chat with Tiny Gordon

Try the following sentences:
```raw
- What is your name?
- How to get the list of the running containers?
- Can you check in the docker documentation?
- ...
```

## Using the API

**Initialize a session**:
```bash
curl -X POST http://localhost:9000/apps/tiny-gordon/users/bob/sessions/bob_session_42 \
  -H "Content-Type: application/json" \
  -d '{"state": {}}' | jq '.'
```

**What is your name?**:
```bash
curl -X POST http://localhost:9000/run \
-H "Content-Type: application/json" \
-d '{
    "appName": "tiny-gordon",
    "userId": "bob",
    "sessionId": "bob_session_42",
    "newMessage": {
        "role": "user",
        "parts": [{
            "text": "What is your name?"
        }]
    }
}' | jq '.'
```

**Containers list**:
```bash
curl -X POST http://localhost:9000/run \
-H "Content-Type: application/json" \
-d '{
    "appName": "tiny-gordon",
    "userId": "bob",
    "sessionId": "bob_session_42",
    "newMessage": {
        "role": "user",
        "parts": [{
            "text": "How to get the list of the running docker containers"
        }]
    }
}' | jq '.'
```

## Development mode using DevContainer
> 👀 look at the `.devcontainer/` directory

### First time - Initialize the Python environment

Start DevContainer.

**Create virtual environment**:
```bash
python -m venv tmp
```
> choose the name you want

**Activate virtual environment**:
```bash
source tmp/bin/activate
```

> **To deactivate virtual environment**
>  ```bash
>  deactivate
>  ```

**Add dependencies**:
```
pip install -r requirements.txt
```

### Start the agent

```bash
# activate the virtual environment: source tmp/bin/activate
adk web
```
> Always use the python virtual environment when running the agent
