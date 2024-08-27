from langchain_groq import ChatGroq
from src.config.appconfig import groq_key

def LLM_Model():
    """This function sets up the LLM model and returns the model.
    Args:
        None.
    Returns:
        class: the LLM model.
    """
    groq_model_name = [
        "mixtral-8x7b-32768",
        "llama3-8b-8192",
        "claude-3-opus-20240229"
    ]
    llm = ChatGroq(
        temperature=0,
        api_key=groq_key,
        model=groq_model_name[1]
    )
    
    return llm
