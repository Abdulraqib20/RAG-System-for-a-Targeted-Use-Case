from typing import Sequence
from langchain.tools import BaseTool
from langchain.prompts import PromptTemplate
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.tools.render import render_text_description
from src.utilities.helpers import get_day_date_month_year_time

class AISoCAgent():
    @classmethod
    def create_prompt(cls, tools: Sequence[BaseTool], system_prompt):
        """
        Create a AISoc Prompt by formatting the system prompt with the dynamic prompt

        Args:
            tools (Sequence[BaseTool]): List of Tools to include in the Prompt
            system_prompt The System prompt template
        
        Returns:
            str: fomatted prompt
        """
        
        AISoC_prompt = PromptTemplate(
            input_variables=[
                'agent_scratchpad',
                'chat_history',
                'input',
                'tool_names',
                'tools'
            ],
            template=system_prompt
        )
        
        # generate the prompt by partially filling template with dynamic values
        return AISoC_prompt.partial(
            tools=render_text_description(tools),
            tool_names=f"Tools: {', '.join([tool.name for tool in tools])}",
            # current_date=get_day_date_month_year_time()[0],
            # current_day_of_the_week=get_day_date_month_year_time()[1],
            # curren_year
            # current_time_hour
            # current_time_min
            # current_time_sec

            # agent_scratchpad=format_log_to_str(tools),
            # input=f"User: {input}"
        )
    
    @classmethod
    def create_prompt_with_user_info(cls, tools: Sequence[BaseTool], system_prompt, name, gender, current_location):
        """
        Create a AISoc prompt by formatting the system prompt with dynamic input.

        Args:
            tools (Sequence[BaseTool]): List of tools to include in the prompt
            system_prompt: System Prompt Template

        Returns:
            str: formatted prompt
        """
        
        AISoC_prompt = PromptTemplate(
            input_variables=[
                'agent_scratchpad',
                'chat_history',
                'input',
                'tool_names',
                'tools',
                'name',
                'gender',
                # 'timezone',
                # 'current_location'
            ],
            template=system_prompt
        )
        return AISoC_prompt.partial(
            tools=render_text_description(tools),
            tool_names=f"Tools: {', '.join([tool.name for tool in tools])}",
            name=name,
            gender=gender,
            # current_location=current_location,
            # current_date=get_day_date_month_year_time()[0],
            # current_day_of_the_week=get_day_date_month_year_time()[1],
            # curren_year
            # current_time_hour
            # current_time_min
            # current_time_sec
        )
    
    @classmethod
    def load_llm_and_tools(
        cls,
        llm,
        tools,
        system_prompt,
        output_parser,
        name,
        gender,
        # timezone,
        # current_location
    ):
        """Load a Language model and tools, create a prompt and parse the output.

        Args:
            llm: language model
            tools (_type_): List of Tools
            system_prompt (_type_): System prompt template
            output_parser (_type_): parse output
        Returns:
            dict: output of the loaded llm and tools.
        """
        if name is None:
            prompt = cls.create_prompt(tools=tools, system_prompt=system_prompt)
        else:
            system_prompt = system_prompt.replace('user', name.split()[0])
            prompt = cls.create_prompt_with_user_info(
                tools=tools,
                system_prompt=system_prompt,
                name=name,
                gender=gender,
                # timezone=timezone,
                # current_location=current_location
            )
            
        llm_with_stop = llm.bind(stop=['\nobservation'])
        return (
            {
                'input': lambda x: x['input'],
                'agent_scratchpad': lambda x: format_log_to_str(
                    x['intermediate_steps']
                ),
                'chat_history': lambda x: x['chat_history']
            }
            | prompt  # apply prompt processing
            | llm_with_stop # apply language model processing
            | output_parser # apply output parsing
        )
      
