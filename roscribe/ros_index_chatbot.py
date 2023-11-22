__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.agents.agent_toolkits import create_retriever_tool
from langchain.agents.agent_toolkits import create_conversational_retrieval_agent
from langchain.chat_models import ChatOpenAI

import roscribe.ui as ui


def main():
    db_name = "ros_index_db_humble_2023_10_31"
    vectorstore = Chroma(persist_directory="ROS_index_database/" + db_name, embedding_function=OpenAIEmbeddings())
    retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={'k': 8})
    
    # Tool Declaration
    tool = create_retriever_tool(
        retriever,
        "search_ROS_repositories",
        "Searches and returns documents regarding the ROS repositories."
    )
    tools = [tool]
    
    # Agent Construction
    llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k", temperature=0)
    agent_executor = create_conversational_retrieval_agent(llm, tools, max_token_limit=6000, verbose=False)
    
    print(ui.WELCOME_MSG_RAG)
    
    while True:
        print('\n\n')
        human_input = input("Input: ")
        result = agent_executor({"input": human_input})
        print('\n\n')
        print(result["output"])


if __name__ == "__main__":
    main()
