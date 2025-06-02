import os

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse, LlmRequest
from typing import Optional, List
#from google.genai import types # For types.Content
from google.genai import types


#from litellm import embedding
#from langchain_core.vectorstores import InMemoryVectorStore
#from langchain_core.embeddings import Embeddings
#from langchain_core.documents import Document


from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

# SETTINGS: needed for the agent to run
os.environ["OPENAI_API_KEY"] = "tada"
os.environ["OPENAI_API_BASE"] = f"{os.environ.get('DMR_BASE_URL')}/engines/llama.cpp/v1"


print("🟡 Initialize...")


# NOTE: this triggered at every request to the agent
def on_request(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    print("⚡️ Request received")
    return None



# AGENT:
root_agent = Agent(
    # SMALL LLM:
    model=LiteLlm(model="openai/" + os.environ.get('MODEL_RUNNER_MODEL')),
    generate_content_config=types.GenerateContentConfig(
        temperature=0.0, # More deterministic output
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
                #'fetch'
            ]
        ),
        MCPToolset(
            connection_params=StdioServerParameters(
                command='./mcp-similarity-search',
                args=[],
            ),
            tool_filter=[
                'docker_command', 
            ]
        ),  
        #MCPToolset(
        #    connection_params=StdioServerParameters(
        #        command='./mcp-talk-to-moby',
        #        args=[],
        #    ),
        #    tool_filter=[
        #        'moby_running_containers', 
        #        'moby_running_all_containers',
        #        'moby_list_all_images',
        #    ]
        #),          
         
    ],
    before_model_callback= on_request,

)

