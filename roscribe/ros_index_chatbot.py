__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.agents.agent_toolkits import create_retriever_tool
from langchain.agents.agent_toolkits import create_conversational_retrieval_agent
from langchain.chat_models import ChatOpenAI


vectorstore = Chroma(persist_directory="./ros_index_db", embedding_function=OpenAIEmbeddings())
retriever = vectorstore.as_retriever(search_type="mmr")

# Tool Declaration
tool = create_retriever_tool(
    retriever,
    "search_ROS_index",
    "Searches and returns documents regarding the ROS index."
)
tools = [tool]

# Agent Construction
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
agent_executor = create_conversational_retrieval_agent(llm, tools, verbose=True)

print('Hi! How can I help you today?')
while True:
    human_input = input()
    result = agent_executor({"input": human_input})
    print(result["output"])
