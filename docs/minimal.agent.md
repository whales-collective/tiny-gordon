

```python
root_agent = Agent(
    model=LiteLlm(model="openai/" + os.environ.get('MODEL_RUNNER_MODEL')),
    generate_content_config=types.GenerateContentConfig(
        temperature=0.0,
    ),
    name="tiny_gordon_agent",
    description=(
        """
        Tiny Gordon agent is a Docker expert.
        """
    ),
    instruction="""
    You are Tiny Gordon, a Docker expert. 
    Use the tools provided to interact with users and give them the best answer. 
    """,
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                command='socat',
                args=[
                    "STDIO",
                    "TCP:host.docker.internal:8811",
                ],
            ),
            tool_filter=['brave_web_search']
        ),
        MCPToolset(
            connection_params=StdioServerParameters(
                command='./mcp-similarity-search',
                args=[
                    "http://model-runner.docker.internal",
                    "ai/mxbai-embed-large:latest",
                    "3",
                ],
            ),
            tool_filter=['question_about_something']
        ),           
    ],
)
```