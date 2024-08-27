
import logging
logger = logging.getLogger(__name__)
from typing import Literal
from src.config.appconfig import Env
from langchain.agents import AgentExecutor
# from src.utilities.messages import *
# from src.utilities.helpers import load_yaml_file

verbose = True

class StreamConversation():
    """A class to handle streaming conversation chain. It creates and stores memory for each conversation and generates
    responses using the LLM
    """
    
    LLM = None
    
    def __init__(self, llm) -> None:
        """
        Initializes the StreamConversation generation.
        """ 
        self.llm = llm
        StreamConversation.LLM=llm
        
    @classmethod
    def create_prompt(
        cls, message:str
    ) -> (tuple[None, None, str] | tuple[None, None, Literal['Something went wrong with retrieving vector store']]
          | tuple[str, AgentExecutor, list, None]):
        
