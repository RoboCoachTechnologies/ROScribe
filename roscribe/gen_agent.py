import os
import pickle

from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import LLMChain

from roscribe.tools import get_rag_tool, get_code_gen_tool, get_code_retrieval_tool
from roscribe.prompts import get_gen_agent_prompt, get_project_name_prompt
from roscribe.spec_agent import load_spec_agent
import roscribe.ui as ui


class GenAgent:
    def __init__(self, ros_distro, ros_graph_dict, ros_node_desc, ws_name='catkin_ws',
                 model_name="gpt-3.5-turbo-0125", max_interaction_limit=6, verbose=False):
        self.ros_distro = ros_distro
        self.model_name = model_name
        self.max_interaction_limit = max_interaction_limit
        self.verbose = verbose

        self.llm = ChatOpenAI(model_name=model_name, temperature=0.1)

        self.ros_graph_dict = ros_graph_dict
        self.ros_node_desc = ros_node_desc

        self.ws_name = ws_name
        self.project_name = None

        rag_tool = get_rag_tool(ros_distro)
        code_gen_tool = get_code_gen_tool(agent=self)
        code_download_tool = get_code_retrieval_tool(agent=self)

        self.tools = [rag_tool, code_gen_tool, code_download_tool]

        self.end_conv_keyword = 'END_OF_GEN'

        self.nodes = dict()
        self.current_node = None

        self.agent_executor = None

    def __call__(self, human_input):
        agent_response = self.agent_executor.invoke({"input": human_input})["output"]
        return agent_response

    def spin(self):
        project_name_prompt = get_project_name_prompt()
        project_name_chain = LLMChain(llm=self.llm, prompt=project_name_prompt, verbose=self.verbose)
        self.project_name = project_name_chain.predict(ros_node_desc=self.ros_node_desc)
        ros_ws_generator(self.project_name, self.ws_name)

        print(ui.GEN_AGENT_WELCOME_MSG)

        for node in self.ros_graph_dict.keys():
            self.current_node = node
            self.reset_agent()
            print(ui.GEN_AGENT_NODE_MSG.format(curr_node=self.current_node))
            agent_response = ""
            while self.end_conv_keyword not in agent_response:
                human_input = input()
                agent_response = self(human_input)
                print(agent_response.replace(self.end_conv_keyword, "") + "\n")

            self.save_code()

        self.save_agent()

    def reset_agent(self):
        agent_prompt = get_gen_agent_prompt(end_conv_keyword=self.end_conv_keyword,
                                            curr_node=self.current_node,
                                            curr_node_desc=self.ros_graph_dict[self.current_node]['description'],
                                            curr_node_sub=self.ros_graph_dict[self.current_node]['subscribed_topics'],
                                            curr_node_pub=self.ros_graph_dict[self.current_node]['published_topics'],
                                            context=self.ros_node_desc)

        agent_memory = ConversationBufferWindowMemory(memory_key="chat_history",
                                                      k=self.max_interaction_limit,
                                                      return_messages=True)

        agent = create_openai_tools_agent(self.llm, self.tools, agent_prompt)
        self.agent_executor = AgentExecutor(agent=agent, tools=self.tools,
                                            memory=agent_memory, verbose=self.verbose)

    def update_node(self, gen_node):
        self.nodes[self.current_node] = gen_node

    def save_code(self):
        code = self.nodes[self.current_node]['code']
        if code != 'RAG':
            filename = f'{self.ws_name}/src/{self.project_name}/src/{self.current_node}.py'
            with open(filename, 'w') as file:
                file.write(code)

    def save_agent(self):
        agent_info = {'project_name': self.project_name,
                      'ws_name': self.ws_name,
                      'nodes': self.nodes,
                      'ros_distro': self.ros_distro,
                      'model_name': self.model_name,
                      'max_interaction_limit': self.max_interaction_limit,
                      'verbose': self.verbose}
        with open('gen_agent.pkl', 'wb') as saved_agent:
            pickle.dump(agent_info, saved_agent, pickle.HIGHEST_PROTOCOL)


def load_gen_agent(gen_agent_filename, spec_agent_filename):
    loaded_spec_agent = load_spec_agent(spec_agent_filename)

    with open(gen_agent_filename, 'rb') as saved_agent:
        loaded_gen_agent_info = pickle.load(saved_agent)

    loaded_gen_agent = GenAgent(ros_distro=loaded_gen_agent_info['ros_distro'],
                                ros_graph_dict=loaded_spec_agent.get_ros_graph_dict(),
                                ros_node_desc=loaded_spec_agent.get_ros_node_desc(),
                                model_name=loaded_gen_agent_info['model_name'],
                                max_interaction_limit=loaded_gen_agent_info['max_interaction_limit'],
                                verbose=loaded_gen_agent_info['verbose'])

    loaded_gen_agent.project_name = loaded_gen_agent_info['project_name']
    loaded_gen_agent.ws_name = loaded_gen_agent_info['ws_name']
    loaded_gen_agent.nodes = loaded_gen_agent_info['nodes']

    return loaded_gen_agent


def ros_ws_generator(project_name, ros_ws_name):
    if not os.path.exists(ros_ws_name):
        os.mkdir(ros_ws_name)

    if not os.path.exists(f'{ros_ws_name}/src'):
        os.mkdir(f'{ros_ws_name}/src')

    os.mkdir(f'{ros_ws_name}/src/{project_name}')
    os.mkdir(f'{ros_ws_name}/src/{project_name}/launch')
    os.mkdir(f'{ros_ws_name}/src/{project_name}/src')
