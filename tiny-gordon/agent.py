import os

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse, LlmRequest
from typing import Optional, List
#from google.genai import types # For types.Content
from google.genai import types


from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

# SETTINGS: needed for the agent to run
#os.environ["OPENAI_API_KEY"] = "tada"
#os.environ["OPENAI_API_BASE"] = f"{os.environ.get('DMR_BASE_URL')}/engines/llama.cpp/v1"


print("🟡 Initialize...")
print(f"🤖 MODEL_RUNNER_MODEL: {os.environ.get('MODEL_RUNNER_MODEL')}")


# NOTE: this triggered at every request to the agent
def on_request(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    print("⚡️ Request received")
    return None


# AGENT:
root_agent = Agent(
    # SMALL LLM:
    model=LiteLlm(
        model=f"openai/{os.environ.get('MODEL_RUNNER_CHAT_MODEL')}",
        api_base=os.environ.get("MODEL_RUNNER_BASE_URL"),
        api_key="tada",
        temperature=0.5,
    ),    
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
    
    tools=[
        MCPToolset(
           connection_params=StdioServerParameters(
               command='./mcp-similarity-search',
               args=[
                   #"http://model-runner.docker.internal",
                   os.environ.get("MODEL_RUNNER_BASE_URL"),
                   #"ai/mxbai-embed-large:latest",
                   os.environ.get("MODEL_RUNNER_EMBEDDING_MODEL"),
                   "3",
               ],
                #3 is the max number of similar documents to return
           ),
           tool_filter=[
               'question_about_something', 
           ]
        ),     
         
    ],
    #before_model_callback= on_request,

)

""" QUESTION:
How to use another agent to generate an answer from the result of the tool?
Check if there is a call back for this.
Have a look to the examples here: https://github.com/hawaiian-pizza-corp/we-are-legion
"""