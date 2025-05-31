import os
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

# DATA: not used for the moment
from .docker_data import docker_data

# SETTINGS: needed for the agent to run
os.environ["OPENAI_API_KEY"] = "tada"
os.environ["OPENAI_API_BASE"] = f"{os.environ.get('DMR_BASE_URL')}/engines/llama.cpp/v1"


# AGENT:
root_agent = Agent(
    # SMALL LLM:
    model=LiteLlm(model="openai/" + os.environ.get('MODEL_RUNNER_MODEL')),

    name="tiny_gordon_agent",
    description=(
        """
        Tiny Gordon agent is a Docker expert.
        """
    ),
    instruction="""
    You are Tiny Gordon, a Docker expert. 
    Use the tools provided to interact with users.
    """,
    # TOOLS CATALOG: with MCP ToolKit
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                command='socat',
                args=[
                    "STDIO",
                    "TCP:host.docker.internal:8811",
                ],
            ),
            # Filter which tools from the MCP server are exposed
            tool_filter=[
                'brave_web_search', 
                'docker',
                'fetch'
            ]
        )
    ],

)
