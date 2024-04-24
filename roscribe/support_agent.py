from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.memory import ConversationBufferWindowMemory

from roscribe.tools import get_rag_tool, get_file_tool
from roscribe.prompts import get_support_agent_prompt
import roscribe.ui as ui


class SupportAgent:
    def __init__(self, ros_distro, ros_graph_dict, ros_nodes, project_name, ws_name, package, dependencies,
                 model_name="gpt-3.5-turbo-0125", max_interaction_limit=6, verbose=False):
        self.ros_distro = ros_distro
        self.model_name = model_name
        self.max_interaction_limit = max_interaction_limit
        llm = ChatOpenAI(model_name=model_name, temperature=0.1)

        self.ros_graph_dict = ros_graph_dict
        self.nodes = ros_nodes

        self.project_name = project_name
        self.ws_name = ws_name

        self.package = package
        self.dependencies = dependencies

        self.verbose = verbose

        rag_tool = get_rag_tool(ros_distro)
        load_file_tool = get_file_tool(agent=self)

        tools = [rag_tool, load_file_tool]

        agent_prompt = get_support_agent_prompt(agent=self)
        agent_memory = ConversationBufferWindowMemory(memory_key="chat_history", k=max_interaction_limit,
                                                      return_messages=True)
        agent = create_openai_tools_agent(llm, tools, agent_prompt)
        self.agent_executor = AgentExecutor(agent=agent, tools=tools, memory=agent_memory, verbose=verbose)

    def __call__(self, human_input):
        agent_response = self.agent_executor.invoke({"input": human_input})["output"]
        return agent_response

    def spin(self):
        print(ui.SUPPORT_AGENT_LAUNCH_MSG)
        while True:
            human_input = input()
            agent_response = self(human_input)
            print(agent_response + "\n")
