from typing import List
import logging

logger = logging.getLogger(__name__)

class AISoCTools:
    
    @classmethod
    def call_tool(cls) -> List:
        """
        Calls the tool based on the specified retreiver.
        
        Parameters:
        - retreiver: optional retreiver to be used

        Returns:
            List of tools to be executed
        """
        try:
            tool_names = []
            tools = cls.tools
            
            for tool in tools:
                tool_names.append(tool.name)
            logger.info(f"""\nTools loaded successfully!\n ----- TOOL REPORT -------\ntoolnames: {str(tool_names)}\nNumber of tools: {len(tool_names)}\n""")
            
            return tools