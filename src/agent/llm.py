from langchain_groq import ChatGroq
from src.config.appconfig import groq_key, openai_api_key, anthropic_key
from langchain_openai import ChatOpenAI
from google.cloud import aiplatform
from anthropic import AnthropicClient

def LLM_Model(provider='groq', model_name=None):
    """
    This function sets up the LLM model and returns the model based on the provider and model name.
    
    Args:
        provider (str): The LLM provider ('groq', 'vertex_ai', 'anthropic', 'openai'). Defaults to 'groq'.
        model_name (str, optional): The name of the model to use. If None, a default model is selected.
        
    Returns:
        class: the LLM model.
    """
    
    # Groq models
    groq_models = {
        "mixtral-8x7b-32768": "mixtral-8x7b-32768",
        "llama3-8b-8192": "llama3-8b-8192",
        "llama3-70b-8192": "llama3-70b-8192",
        "llama-3.1-70b-versatile": "llama-3.1-70b-versatile"
    }

    # Vertex AI models (via Google Cloud Platform)
    vertex_ai_models = {
        "gemini-1.5-pro-001": "gemini-1.5-pro-001",
        "mistral-large@2407": "mistral-large@2407"
    }

    # Anthropic models (via GCP's AnthropicVertex)
    anthropic_models = {
        "claude-3-opus@20240229": "claude-3-opus@20240229",
        "claude-3-5-sonnet@20240620": "claude-3-5-sonnet@20240620"
    }

    # OpenAI models (optional)
    openai_models = {
        "gpt-4o": "gpt-4o",
        "gpt-4o-mini": "gpt-4o-mini"
    }

    # Groq Model Setup
    if provider == 'groq':
        model = model_name if model_name else groq_models['llama3-8b-8192']
        llm = ChatGroq(
            temperature=0.2,
            api_key=groq_key,
            model=model,
            max_retries=5
        )

    # # Vertex AI Model Setup
    # elif provider == 'vertex_ai':
    #     model = model_name if model_name else vertex_ai_models['gemini-1.5-pro-001']
    #     # Assuming aiplatform is properly configured with service account, key, etc.
    #     aiplatform.init(project="your-gcp-project", location="us-central1")
    #     llm = aiplatform.Model(model).deploy()

    # # Anthropic Model Setup
    # elif provider == 'anthropic':
    #     model = model_name if model_name else anthropic_models['claude-3-opus@20240229']
    #     llm = AnthropicClient(api_key=anthropic_key, model=model)

    # OpenAI Model Setup (optional)
    elif provider == 'openai':
        model = model_name if model_name else openai_models['gpt-4o']
        llm = ChatOpenAI(
            api_key=openai_api_key,
            model=model,
            temperature=0.2,
            max_retries=5
        )

    else:
        raise ValueError(f"Unsupported provider: {provider}")

    return llm

# LLM_Model(provider='groq', model_name='llama3-70b-8192')
# LLM_Model(provider='vertex_ai', model_name='gemini-1.5-pro-001')
# LLM_Model(provider='openai', model_name='gpt-4o')


# def LLM_Model():
#     """This function sets up the LLM model and returns the model.
#     Args:
#         None.
#     Returns:
#         class: the LLM model.
#     """
#     groq_model_name = [
#         "mixtral-8x7b-32768",
#         "llama3-8b-8192",
#         "llama3-70b-8192",
#         "claude-3-opus-20240229"
#     ]
#     llm = ChatGroq(
#         temperature=0.2,
#         api_key=groq_key,
#         model=groq_model_name[1], 
#         max_retries=5
#     )
    
#     return llm

