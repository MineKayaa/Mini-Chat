from langchain_openai import ChatOpenAI
from langchain.agents import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import AgentExecutor
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

llm= ChatOpenAI(temperature=0, model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY)

@tool
def find_save_word(input: str) -> bool:
    """Find the Save To VectorDB in given input
        Args:
            input: human question
        Returns:
            bool 
        """
    if "Save To VectorDB" in input: 
        return True
    else :
        return False

tools = [find_save_word]

class utils:
    def get_model():
        return llm
    def get_agent(input : str, chat_history : str) :
        llm_with_tools = llm.bind_tools(tools)
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful assistant. Here is the chat history {chat_history}.",
                ),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )
        agent = (
            {
                "input": lambda x: x["input"],
                "chat_history": lambda x: x["chat_history"],
                "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                    x["intermediate_steps"]
                ),
            }
            | prompt
            | llm_with_tools
            | OpenAIToolsAgentOutputParser()
        )

        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        output = agent_executor.invoke({"input": input,"chat_history" : chat_history })

        print(output)
        return output['output']
    
