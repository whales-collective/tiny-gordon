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



# NOTE: this triggered at every request to the agent
def on_request(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    print("⚡️ Request received")
    return None

def generate_embeddings() -> str:
    """
    Generate embeddings for the documents and add them to the vector store.
    """
    print("🟠 Generating embeddings...")
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

    print("🟢 Embeddings generated and stored in vector_store.")

    return "Embeddings generated and stored in vector_store."

# TOOL:
def look_at_internal_db(question: str) -> list[Document]:
    """
    Look at the internal database for similarities with the user's question.
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

    To generate embeddings, use the 'generate_embeddings' tool.
    
    To search information about docker use the 'look_at_internal_db' tool with the complete user question as the parameter.
    If the 'look_at_internal_db' tool returns content, use that content to make the answer.
    
    Example: 
    If the user says 'give me the list of running containers', 
    call look_at_internal_db('give me the list of running containers').

    to execute commands related to docker, use these tools:
    - 'moby_running_containers': to list running containers
    - 'moby_running_all_containers': to list all containers
    - 'moby_list_all_images': to list all images

    If the user asks for a web search, use the 'brave_web_search' tool.

    Format your responses in markdown.
    Use only Latin characters. Do not use Chinese, Japanese, or Korean characters.

    Use only the information provided above to answer. 
    Do not use any external knowledge or information from your training data. 
    If the answer cannot be found in the provided data, reply ‘I don’t know.’

    """,
    # TOOLS CATALOG: with MCP ToolKit
    tools=[
        look_at_internal_db,
        generate_embeddings,
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
        ),
        MCPToolset(
            connection_params=StdioServerParameters(
                command='./mcp-talk-to-moby',
                args=[],
            ),
            tool_filter=[
                'moby_running_containers', 
                'moby_running_all_containers',
                'moby_list_all_images',
            ]
        ),        
    ],
    before_model_callback= on_request,

)

