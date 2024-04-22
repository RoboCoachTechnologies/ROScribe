__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import graphviz as gv
import re, subprocess

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import LLMChain
from langchain.agents import tool
from langchain.agents.agent_toolkits import create_retriever_tool

from roscribe.prompts import get_gen_code_prompt, get_edit_code_prompt,\
    get_gen_launch_prompt, get_edit_launch_prompt, get_gen_package_prompt, get_edit_package_prompt,\
    get_gen_cmake_prompt, get_edit_cmake_prompt, get_gen_readme_prompt, get_edit_readme_prompt


def get_rag_tool(ros_distro):
    db_name = "ros_index_db_{}".format(ros_distro)
    vectorstore = Chroma(persist_directory="ROS_index_database/" + db_name, embedding_function=OpenAIEmbeddings())
    retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={'k': 8})

    rag_tool = create_retriever_tool(
        retriever,
        "search_ROS_repositories",
        "Searches and returns documents regarding the ROS repositories."
    )

    return rag_tool


def get_gen_graph_tool(agent):
    @tool
    def show_ROS_graph() -> str:
        """Shows the ROS Graph and generates a description of the ROS Graph in natural language."""

        ros_graph_dict = agent.predict_ros_graph_dict()

        if not isinstance(ros_graph_dict, dict) or len(ros_graph_dict.keys()) == 0:
            return "The graph is empty since there hasn't been enough conversation with the human user."

        graph = gv.Digraph()
        graph.attr(rankdir='LR')

        topic_list = []

        for node in ros_graph_dict.keys():
            graph.node(node, style='solid', color='black', shape='ellipse')

            for sub_topic in ros_graph_dict[node]['subscribed_topics']:
                if sub_topic not in topic_list:
                    topic_list.append(sub_topic)
                    graph.node(sub_topic, style='solid', color='black', shape='box')
                graph.edge(sub_topic, node)

            for pub_topic in ros_graph_dict[node]['published_topics']:
                if pub_topic not in topic_list:
                    topic_list.append(pub_topic)
                    graph.node(pub_topic, style='solid', color='black', shape='box')
                graph.edge(node, pub_topic)

        graph.view()

        gen_msg = "Here is a description of the shown ROS Graph:\n" + agent.get_ros_node_desc()

        return gen_msg

    return show_ROS_graph


def get_code_gen_tool(agent):
    @tool
    def write_ros_node(coding_task: str) -> str:
        """Takes a very detailed coding task in natural language and implements the code in python."""

        if agent.current_node not in agent.nodes.keys():
            gen_code_prompt = get_gen_code_prompt()
        else:
            if agent.nodes[agent.current_node]['code'] == 'RAG':
                return "There is no need to generate code for this ROS node!"
            else:
                gen_code_prompt = get_edit_code_prompt(code=agent.nodes[agent.current_node]['code'])

        gen_code_chain = LLMChain(llm=agent.llm, prompt=gen_code_prompt, verbose=agent.verbose)
        gen_code_output = gen_code_chain.predict(task=coding_task)

        parsed_output, successful = parse_code_gen(gen_code_output)

        if successful:
            agent.update_node(parsed_output)

            gen_msg = "Python implementation of the ROS node:\n{code}\n\n{readme}".format(
                                                                                   code=parsed_output['code'],
                                                                                   readme=parsed_output['readme'])
            ret_msg = "Python implementation of the ROS node is successfully done!"
        else:
            gen_msg = "Python implementation of the ROS node was unsuccessful!"
            ret_msg = gen_msg

        print(gen_msg)
        return ret_msg

    return write_ros_node


def get_code_retrieval_tool(agent):
    @tool
    def download_code(checkout_uri: str, vcs_version: str) -> str:
        """Takes checkout URI and VCS version of a GitHub repository, and downloads the code."""

        regex = r"\/(\w+)\.git"
        matches = re.findall(regex, checkout_uri)

        try:
            repo_name = matches[0]
        except IndexError:
            return "Code download was unsuccessful due to incorrect Git URI.\n" \
                   "Make sure the 'checkout_uri' is a Git URI.\n" \
                   "Instead, set the search query to 'Repository summary for REPO_NAME' where REPO_NAME is the name of the repository."

        git_command = "git clone {uri} -b {ver}".format(uri=checkout_uri, ver=vcs_version)

        print(f'Downloading code for {repo_name} using:\n{git_command}')

        try:
            subprocess.check_output(f'cd {agent.ws_name}/src && {git_command}', shell=True)
            ret_msg = f'Code for {repo_name} successfully downloaded in the ROS workspace!'

            node_info = {'code': 'RAG', 'readme': f'{repo_name}'}
            agent.update_node(node_info)

        except subprocess.CalledProcessError:
            ret_msg = f'Code download for {repo_name} was unsuccessful!'

        print(ret_msg)
        return ret_msg

    return download_code


def get_launch_tool(agent):
    @tool
    def edit_launch_file(launch_file_edit_task: str) -> str:
        """Takes feedback in natural language from the agent in order to edit a ROS launch file."""

        if agent.package[f'{agent.project_name}.launch'] is None:
            gen_launch_prompt = get_gen_launch_prompt(agent=agent)
            edit = False
        else:
            gen_launch_prompt = get_edit_launch_prompt(launch_file=agent.package[f'{agent.project_name}.launch'])
            edit = True

        gen_launch_chain = LLMChain(llm=agent.llm, prompt=gen_launch_prompt, verbose=agent.verbose)

        if edit:
            gen_launch_output = gen_launch_chain.predict(task=launch_file_edit_task)
        else:
            gen_launch_output = gen_launch_chain.predict()

        parsed_output, successful = parse_code_gen(gen_launch_output)

        if successful:
            agent.package[f'{agent.project_name}.launch'] = parsed_output['code']

            gen_msg = "Generated ROS launch file for the ROS package:\n{launch_file}"\
                .format(launch_file=parsed_output['code'])

            ret_msg = "The ROS launch file for the ROS package has been successfully edited!"
        else:
            gen_msg = "Modification of the ROS launch file for the ROS package was unsuccessful!"
            ret_msg = gen_msg

        if edit:
            print(gen_msg)

        return ret_msg

    return edit_launch_file


def get_package_tool(agent):
    @tool
    def edit_package_xml(ros_package_edit_task: str) -> str:
        """Takes feedback in natural language from the agent in order to edit a ROS package.xml file."""

        if agent.package['package.xml'] is None:
            gen_package_prompt = get_gen_package_prompt(agent=agent)
            edit = False
        else:
            gen_package_prompt = get_edit_package_prompt(package=agent.package['package.xml'])
            edit = True

        gen_package_chain = LLMChain(llm=agent.llm, prompt=gen_package_prompt, verbose=agent.verbose)

        if edit:
            gen_package_output = gen_package_chain.predict(task=ros_package_edit_task)
        else:
            gen_package_output = gen_package_chain.predict()

        parsed_output, successful = parse_code_gen(gen_package_output)

        if successful:
            agent.package['package.xml'] = parsed_output['code']

            gen_msg = "Generated package.xml for the ROS package:\n{package}".format(package=parsed_output['code'])

            ret_msg = "The package.xml file for the ROS package has been successfully edited!"
        else:
            gen_msg = "Modification of the package.xml file for the ROS package was unsuccessful!"
            ret_msg = gen_msg

        if edit:
            print(gen_msg)

        return ret_msg

    return edit_package_xml


def get_cmake_tool(agent):
    @tool
    def edit_cmake(ros_cmake_edit_task: str) -> str:
        """Takes feedback in natural language from the agent in order to edit a CMakeLists.txt file for a ROS package."""

        if agent.package['CMakeLists.txt'] is None:
            gen_cmake_prompt = get_gen_cmake_prompt(agent)
            edit = False
        else:
            gen_cmake_prompt = get_edit_cmake_prompt(cmake=agent.package['CMakeLists.txt'])
            edit = True

        gen_cmake_chain = LLMChain(llm=agent.llm, prompt=gen_cmake_prompt, verbose=agent.verbose)

        if edit:
            gen_cmake_output = gen_cmake_chain.predict(task=ros_cmake_edit_task)
        else:
            gen_cmake_output = gen_cmake_chain.predict()

        parsed_output, successful = parse_code_gen(gen_cmake_output)

        if successful:
            agent.package['CMakeLists.txt'] = parsed_output['code']

            gen_msg = "Generated CMakeLists.txt for the ROS package:\n{cmake}".format(cmake=parsed_output['code'])

            ret_msg = "The CMakeLists.txt file for the ROS package has been successfully edited!"
        else:
            gen_msg = "Modification of the CMakeLists.txt file for the ROS package was unsuccessful!"
            ret_msg = gen_msg

        if edit:
            print(gen_msg)

        return ret_msg

    return edit_cmake


def get_readme_tool(agent):
    @tool
    def edit_readme(ros_readme_edit_task: str) -> str:
        """Takes feedback in natural language from the agent in order to edit a README.md file for a ROS package."""

        if agent.package['README.md'] is None:
            gen_readme_prompt = get_gen_readme_prompt(agent)
            edit = False
        else:
            gen_readme_prompt = get_edit_readme_prompt(readme=agent.package['README.md'])
            edit = True

        gen_readme_chain = LLMChain(llm=agent.llm, prompt=gen_readme_prompt, verbose=agent.verbose)

        if edit:
            gen_readme_output = gen_readme_chain.predict(task=ros_readme_edit_task)
        else:
            gen_readme_output = gen_readme_chain.predict()

        parsed_output, successful = parse_code_gen(gen_readme_output)

        if successful:
            agent.package['README.md'] = parsed_output['code']

            gen_msg = "Generated README.md for the ROS package:\n{readme}".format(readme=parsed_output['code'])

            ret_msg = "The README.md file for the ROS package has been successfully edited!"
        else:
            gen_msg = "Modification of the README.md file for the ROS package was unsuccessful!"
            ret_msg = gen_msg

        if edit:
            print(gen_msg)

        return ret_msg

    return edit_readme


def get_file_tool(agent):
    @tool
    def load_file(file_name: str) -> str:
        """Takes a file name and loads the content of the file."""

        file_address = f"{agent.ws_name}/src/{agent.project_name}/"

        if '.py' in file_name:
            file_name = file_address + "src/" + file_name
        elif '.launch' in file_name:
            file_name = file_address + "launch/" + file_name
        else:
            file_name = file_address + file_name

        try:
            f = open(file_name, "r")
            content = f.read()
            return content
        except OSError:
            return "File cannot be opened! It can be due to an incorrect file name, or the file might be missing!"

    return load_file


def parse_code_gen(code_gen_output):
    regex = r"```[^\n]*\n(.+?)```"
    match = re.match(regex, code_gen_output, re.DOTALL)

    if match is None:
        return {'code': 'Generated code cannot be parsed!', 'readme': 'Generated README cannot be parsed!'}, False

    code = match.group(1)
    readme = code_gen_output.split("```")[-1]

    return {'code': code, 'readme': readme}, True
