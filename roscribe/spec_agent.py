import pickle
import ast

from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import LLMChain

from roscribe.tools import get_rag_tool, get_gen_graph_tool
from roscribe.prompts import get_spec_agent_prompt, get_node_desc_prompt, get_graph_gen_prompt
import roscribe.ui as ui


class SpecAgent:
    def __init__(self, ros_distro, model_name="gpt-3.5-turbo-0125", max_interaction_limit=6, verbose=False):
        llm = ChatOpenAI(model_name=model_name, temperature=0.1)

        self.ros_distro = ros_distro
        self.model_name = model_name
        self.max_interaction_limit = max_interaction_limit
        self.verbose = verbose

        rag_tool = get_rag_tool(ros_distro)
        ros_graph_tool = get_gen_graph_tool(agent=self)

        tools = [rag_tool, ros_graph_tool]

        self.end_conv_keyword = 'END_OF_SPEC'
        agent_prompt = get_spec_agent_prompt(end_conv_keyword=self.end_conv_keyword)
        agent_memory = ConversationBufferWindowMemory(memory_key="chat_history", k=max_interaction_limit,
                                                      return_messages=True)
        agent = create_openai_tools_agent(llm, tools, agent_prompt)
        self.agent_executor = AgentExecutor(agent=agent, tools=tools, memory=agent_memory, verbose=verbose)

        node_desc_prompt = get_node_desc_prompt()
        self.node_desc_chain = LLMChain(llm=llm, prompt=node_desc_prompt, verbose=verbose)
        self.ros_node_desc = "No ROS node description has been generated yet!"

        graph_gen_prompt = get_graph_gen_prompt()
        self.graph_gen_chain = LLMChain(llm=llm, prompt=graph_gen_prompt, verbose=verbose)
        self.ros_graph = dict()

    def __call__(self, human_input):
        self.ros_node_desc = self.node_desc_chain.predict(input=human_input, chat_history=self.get_conv_from_memory(),
                                                          ros_node_desc=self.ros_node_desc)

        agent_response = self.agent_executor.invoke({"input": human_input})["output"]

        return agent_response

    def spin(self):
        print(ui.SPEC_AGENT_WELCOME_MSG)
        agent_response = ""
        while self.end_conv_keyword not in agent_response:
            human_input = input()
            agent_response = self(human_input)
            print(agent_response.replace(self.end_conv_keyword, "") + "\n")

        self.save_agent()

    def predict_ros_graph_dict(self):
        ros_graph_llm = self.graph_gen_chain.predict(ros_node_desc=self.ros_node_desc)
        ros_graph_llm_cleaned = cleanup_string_before_eval(ros_graph_llm)

        try:
            self.ros_graph = ast.literal_eval(ros_graph_llm_cleaned)
            return self.ros_graph
        except SyntaxError:
            return "ROS graph parsing was unsuccessful!"

    def get_ros_node_desc(self):
        return self.ros_node_desc

    def get_ros_graph_dict(self):
        return self.ros_graph

    def get_conv_from_memory(self):
        self.agent_executor.memory.return_messages = False
        conv_str = self.agent_executor.memory.buffer
        self.agent_executor.memory.return_messages = True
        return conv_str

    def save_agent(self):
        agent_info = {'ros_graph_dict': self.predict_ros_graph_dict(),
                      'ros_node_desc': self.get_ros_node_desc(),
                      'ros_distro': self.ros_distro,
                      'model_name': self.model_name,
                      'max_interaction_limit': self.max_interaction_limit,
                      'verbose': self.verbose}
        with open('spec_agent.pkl', 'wb') as saved_agent:
            pickle.dump(agent_info, saved_agent, pickle.HIGHEST_PROTOCOL)


def load_spec_agent(filename):
    with open(filename, 'rb') as saved_agent:
        loaded_spec_agent_info = pickle.load(saved_agent)

    loaded_spec_agent = SpecAgent(ros_distro=loaded_spec_agent_info['ros_distro'],
                                  model_name=loaded_spec_agent_info['model_name'],
                                  max_interaction_limit=loaded_spec_agent_info['max_interaction_limit'],
                                  verbose=loaded_spec_agent_info['verbose'])

    loaded_spec_agent.ros_graph = loaded_spec_agent_info['ros_graph_dict']
    loaded_spec_agent.ros_node_desc = loaded_spec_agent_info['ros_node_desc']

    return loaded_spec_agent


def cleanup_string_before_eval(input_str):
    return input_str.replace('\n', '').replace('(', '{').replace(')', '}').replace('robot\'s', 'robot')\
        .replace('user\'s', 'user')

