import ast
import pickle

from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import LLMChain

from roscribe.tools import get_rag_tool, get_launch_tool, get_package_tool, get_cmake_tool, get_readme_tool
from roscribe.prompts import get_dep_prompt, get_launch_agent_prompt, get_package_agent_prompt,\
    get_cmake_agent_prompt, get_readme_agent_prompt
from roscribe.spec_agent import load_spec_agent
from roscribe.gen_agent import load_gen_agent
import roscribe.ui as ui


class PackAgent:
    def __init__(self, ros_distro, ros_graph_dict, ros_node_desc, ros_nodes, project_name, ws_name,
                 model_name="gpt-3.5-turbo-0125", max_interaction_limit=6, verbose=False):
        self.ros_distro = ros_distro
        self.model_name = model_name
        self.max_interaction_limit = max_interaction_limit
        self.llm = ChatOpenAI(model_name=model_name, temperature=0.1)

        self.ros_graph_dict = ros_graph_dict
        self.ros_node_desc = ros_node_desc
        self.nodes = ros_nodes

        self.project_name = project_name
        self.ws_name = ws_name

        self.verbose = verbose

        self.package = {f'{project_name}.launch': None,
                        'README.md': None,
                        'package.xml': None,
                        'CMakeLists.txt': None}

        self.dependencies = []

        self.end_conv_keyword = 'END_OF_PACK'

        self.agent_executor = None

    def __call__(self, human_input):
        agent_response = self.agent_executor.invoke({"input": human_input})["output"]
        return agent_response

    def spin(self):
        find_dep_prompt = get_dep_prompt()
        find_dep_chain = LLMChain(llm=self.llm, prompt=find_dep_prompt, verbose=self.verbose)

        for node in self.nodes:
            if self.nodes[node]['code'] != 'RAG':
                code = self.nodes[node]['code']
                find_dep_output = find_dep_chain.predict(code=code)
                self.dependencies.extend(ast.literal_eval(find_dep_output))

        self.init_launch_agent()
        print(ui.PACK_AGENT_LAUNCH_MSG.format(launch=self.package[f'{self.project_name}.launch']))
        agent_response = ""
        while self.end_conv_keyword not in agent_response:
            human_input = input()
            agent_response = self(human_input)
            print(agent_response.replace(self.end_conv_keyword, "") + "\n")

        self.save_file(f'{self.project_name}.launch')

        self.init_package_agent()
        print(ui.PACK_AGENT_PACKAGE_MSG.format(package=self.package['package.xml']))
        agent_response = ""
        while self.end_conv_keyword not in agent_response:
            human_input = input()
            agent_response = self(human_input)
            print(agent_response.replace(self.end_conv_keyword, "") + "\n")

        self.save_file('package.xml')

        self.init_cmake_agent()
        print(ui.PACK_AGENT_CMAKE_MSG.format(cmake=self.package['CMakeLists.txt']))
        agent_response = ""
        while self.end_conv_keyword not in agent_response:
            human_input = input()
            agent_response = self(human_input)
            print(agent_response.replace(self.end_conv_keyword, "") + "\n")

        self.save_file('CMakeLists.txt')

        self.init_readme_agent()
        print(ui.PACK_AGENT_README_MSG.format(readme=self.package['README.md']))
        agent_response = ""
        while self.end_conv_keyword not in agent_response:
            human_input = input()
            agent_response = self(human_input)
            print(agent_response.replace(self.end_conv_keyword, "") + "\n")

        self.save_file('README.md')

        self.save_agent()

    def save_file(self, file_type):
        if 'launch' in file_type:
            filename = f'{self.ws_name}/src/{self.project_name}/launch/{file_type}'
        else:
            filename = f'{self.ws_name}/src/{self.project_name}/{file_type}'

        with open(filename, 'w') as file:
            file.write(self.package[file_type])

    def init_launch_agent(self):
        rag_tool = get_rag_tool(self.ros_distro)
        launch_edit_tool = get_launch_tool(agent=self)

        tools = [rag_tool, launch_edit_tool]

        launch_edit_tool("")

        agent_prompt = get_launch_agent_prompt(agent=self)

        agent_memory = ConversationBufferWindowMemory(memory_key="chat_history",
                                                      k=self.max_interaction_limit,
                                                      return_messages=True)

        agent = create_openai_tools_agent(self.llm, tools, agent_prompt)
        self.agent_executor = AgentExecutor(agent=agent, tools=tools,
                                            memory=agent_memory, verbose=self.verbose)

    def init_package_agent(self):
        package_edit_tool = get_package_tool(agent=self)

        tools = [package_edit_tool]

        package_edit_tool("")

        agent_prompt = get_package_agent_prompt(agent=self)

        agent_memory = ConversationBufferWindowMemory(memory_key="chat_history",
                                                      k=self.max_interaction_limit,
                                                      return_messages=True)

        agent = create_openai_tools_agent(self.llm, tools, agent_prompt)
        self.agent_executor = AgentExecutor(agent=agent, tools=tools,
                                            memory=agent_memory, verbose=self.verbose)

    def init_cmake_agent(self):
        cmake_edit_tool = get_cmake_tool(agent=self)

        tools = [cmake_edit_tool]

        cmake_edit_tool("")

        agent_prompt = get_cmake_agent_prompt(agent=self)

        agent_memory = ConversationBufferWindowMemory(memory_key="chat_history",
                                                      k=self.max_interaction_limit,
                                                      return_messages=True)

        agent = create_openai_tools_agent(self.llm, tools, agent_prompt)
        self.agent_executor = AgentExecutor(agent=agent, tools=tools,
                                            memory=agent_memory, verbose=self.verbose)

    def init_readme_agent(self):
        readme_edit_tool = get_readme_tool(agent=self)

        tools = [readme_edit_tool]

        readme_edit_tool("")

        agent_prompt = get_readme_agent_prompt(agent=self)

        agent_memory = ConversationBufferWindowMemory(memory_key="chat_history",
                                                      k=self.max_interaction_limit,
                                                      return_messages=True)

        agent = create_openai_tools_agent(self.llm, tools, agent_prompt)
        self.agent_executor = AgentExecutor(agent=agent, tools=tools,
                                            memory=agent_memory, verbose=self.verbose)

    def save_agent(self):
        agent_info = {'package': self.package,
                      'dependencies': self.dependencies,
                      'ros_distro': self.ros_distro,
                      'model_name': self.model_name,
                      'max_interaction_limit': self.max_interaction_limit,
                      'verbose': self.verbose}
        with open('pack_agent.pkl', 'wb') as saved_agent:
            pickle.dump(agent_info, saved_agent, pickle.HIGHEST_PROTOCOL)


def load_pack_agent(pack_agent_filename, gen_agent_filename, spec_agent_filename):
    loaded_spec_agent = load_spec_agent(spec_agent_filename)
    loaded_gen_agent = load_gen_agent(gen_agent_filename, spec_agent_filename)

    with open(pack_agent_filename, 'rb') as saved_agent:
        loaded_pack_agent_info = pickle.load(saved_agent)

    loaded_pack_agent = PackAgent(ros_distro=loaded_pack_agent_info['ros_distro'],
                                  ros_graph_dict=loaded_spec_agent.get_ros_graph_dict(),
                                  ros_node_desc=loaded_spec_agent.get_ros_node_desc(),
                                  model_name=loaded_pack_agent_info['model_name'],
                                  max_interaction_limit=loaded_pack_agent_info['max_interaction_limit'],
                                  verbose=loaded_pack_agent_info['verbose'],
                                  project_name=loaded_gen_agent.project_name,
                                  ros_nodes=loaded_gen_agent.nodes,
                                  ws_name=loaded_gen_agent.ws_name)

    loaded_pack_agent.package = loaded_pack_agent_info['package']
    loaded_pack_agent.dependencies = loaded_pack_agent_info['dependencies']

    return loaded_pack_agent
