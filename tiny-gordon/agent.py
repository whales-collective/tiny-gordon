import os

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse, LlmRequest
from typing import Optional, List
#from google.genai import types # For types.Content
from google.genai import types


from litellm import embedding
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document


from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

# DATA: not used for the moment
from .docker_data import docker_data

# SETTINGS: needed for the agent to run
os.environ["OPENAI_API_KEY"] = "tada"
os.environ["OPENAI_API_BASE"] = f"{os.environ.get('DMR_BASE_URL')}/engines/llama.cpp/v1"


print("🟡 Initialize...")

# HELPER: LiteLLM Embedding Wrapper (custom embedding class)
class LiteLLMEmbeddingWrapper(Embeddings):
    def __init__(self):
        self.model = "openai/" + os.environ.get('MODEL_RUNNER_EMBEDDING_MODEL')
        self.api_base = f"{os.environ.get('DMR_BASE_URL')}/engines/llama.cpp/v1"

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        response = embedding(
            model=self.model,
            api_key="tada",  # Your API key
            api_base=self.api_base,
            input=texts
        )
        return [e['embedding'] for e in response.data]

    def embed_query(self, text: str) -> List[float]:
        return self.embed_documents([text])[0]


# VECTOR STORE: Initialize vector store with your embeddings
embeddings = LiteLLMEmbeddingWrapper()
vector_store = InMemoryVectorStore(embedding=embeddings)


print("🟠 List of the documents:")
# Loop through docs and create embeddings
inputs_outputs = []

for document in docker_data:

    input_val = document.get('input', '') or ''
    output_val = document.get('output', '') or ''
    
    element = f"input: {input_val}\noutput: {output_val}"
    print(element)
    print("-" * 50)  # separator

    inputs_outputs.append(element)


# DOCUMENTS: Add documents: convert star_trek_docs to Document objects
documents = [Document(page_content=text, metadata={}) for text in inputs_outputs]

# DATA: you can add them to the vector store
vector_store.add_documents(documents=documents)

print("🟢 Vectors ready")

# NOTE: this triggered at every request to the agent
def on_request(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    print("⚡️ Request received")
    return None

# TOOL:
def look_at_internal_db(question: str):
    """
    Use the entire user question to search for similarities.
    Args:
        question (str): The full question asked by the user, unmodified.
    Returns:
        list: The list of similarities found.
    """

    print(f"🔎 Searching for similarities with question: {question}")

    # Perform similarity search
    results = vector_store.similarity_search(question, k=3)

    return results



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
    
    First use the 'look_at_internal_db' tool with the complete user question as the parameter.
    If the 'look_at_internal_db' tool returns content, use that content to make the answer.
    
    Example: 
    If the user says 'give me the list of running containers', 
    call look_at_internal_db('give me the list of running containers').

    Then use the complete user question as the parameter of the 'brave_web_search' tool.
    If the 'brave_web_search' tool returns results, use that content to make the answer.
    Always display the source of the information in the answer.

    Format your responses in markdown, only in english.
    """,
    # TOOLS CATALOG: with MCP ToolKit
    tools=[
        look_at_internal_db,
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
                'fetch'
            ]
        )
    ],
    before_model_callback= on_request,

)

    