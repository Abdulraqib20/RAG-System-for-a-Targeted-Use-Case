import logging
from src.agent.base.agenthead import AISoCAgent
from src.agent.base.parser import ReActSingleInputOutputParser
from src.agent.toolkit.base import AISoCTools
from src.prompts import instruction
logger = logging.getLogger(__name__)
from typing import Literal
from src.config.appconfig import Env
from langchain.agents import AgentExecutor
from datetime import datetime
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

        """
        Asynchronously generate a prompt for the conversation.
        
        Args:
            message (str): The message to generate the prompt for.
        
        Returns:
            Tuple: A tuple containing message, agent_executor, chat_history, and error term if any.
        """
        
        try:
            chat_history = []
            updated_tools = AISoCTools.call_tool()
            INST_PROMPT = instruction.INSTPROMPT
            
            # Format the INST_PROMPT with current date and time
            current_datetime = datetime.now()
            INST_PROMPT = INST_PROMPT.format(
                current_date=current_datetime.strftime("%Y-%m-%d"),
                current_day_of_the_week=current_datetime.strftime("%A"),
                current_year=current_datetime.strftime("%Y"),
                current_time=current_datetime.strftime("%H:%M:%S"),
                # name="User",
                # gender="Unknown",
                # current_location="Unknown",
                tools=", ".join([tool.name for tool in updated_tools]),
                tool_names=", ".join([tool.name for tool in updated_tools]),
                chat_history=chat_history,
                input=message
            )
            
            agent = AISoCAgent.load_llm_and_tools(
                cls=cls.LLM,
                tools=updated_tools,
                system_prompt=INST_PROMPT,
                output_parser=ReActSingleInputOutputParser()
            )
            
            agent_executor = AgentExecutor(
                agent=agent,
                tools=updated_tools,
                max_iterations=8,
                handle_parsing_errors=True,
                verbose=verbose
            )
            
            return message, agent_executor, chat_history, None
        
        except Exception as e:
            logger.error(f"Error occurred while creating prompt: {str(e)}")
            return message, None, chat_history, "Something went wrong with retrieving vector store"
        
        
    @classmethod
    async def agenerate(
        cls, message: str, agent_executor: AgentExecutor, chat_history: list
    ) -> str:
        """
        Asynchronously generate a response using the agent executor.
        
        Args:
            message (str): The input message.
            agent_executor (AgentExecutor): The agent executor to use.
            chat_history (list): The chat history.
        
        Returns:
            str: The generated response.
        """
        try:
            response = await agent_executor.arun(input=message)
            return response
        except Exception as e:
            logger.error(f"Error in agenerate: {str(e)}")
            return "I apologize, but I encountered an error while processing your request. Please try again."

    @classmethod
    def generate(
        cls, message: str, agent_executor: AgentExecutor, chat_history: list
    ) -> str:
        """
        Generate a response using the agent executor.
        
        Args:
            message (str): The input message.
            agent_executor (AgentExecutor): The agent executor to use.
            chat_history (list): The chat history.
        
        Returns:
            str: The generated response.
        """
        try:
            response = agent_executor.run(input=message)
            return response
        except Exception as e:
            logger.error(f"Error in generate: {str(e)}")
            return "I apologize, but I encountered an error while processing your request. Please try again."
