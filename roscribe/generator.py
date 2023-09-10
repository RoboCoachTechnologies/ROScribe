import os

from langchain.chains import LLMChain

from roscribe.prompt import get_gen_code_prompt, get_gen_launch_prompt,\
    get_gen_cmake_prompt, get_gen_package_prompt
from roscribe.parser import get_code_from_chat

import roscribe.ui as ui


def catkin_ws_generator(project_name):
    if not os.path.exists('catkin_ws'):
        os.mkdir('catkin_ws')

    if not os.path.exists('catkin_ws/src'):
        os.mkdir('catkin_ws/src')

    os.mkdir(f'catkin_ws/src/{project_name}')
    os.mkdir(f'catkin_ws/src/{project_name}/src')
    os.mkdir(f'catkin_ws/src/{project_name}/launch')


def code_generator(task, node_topic_list, curr_node, summary, project_name, llm, verbose=False):
    gen_code_prompt = get_gen_code_prompt()

    gen_code_chain = LLMChain(
        llm=llm,
        prompt=gen_code_prompt,
        verbose=verbose
    )

    gen_code_output = gen_code_chain.predict(task=task, node_topic_list=node_topic_list,
                                             curr_node=curr_node, summary=summary)

    to_files(gen_code_output, project_name, 'src')

    print(ui.GEN_NODE_CODE_MSG.format(node=curr_node))


def launch_generator(task, node_topic_list, project_name, llm, verbose=False):
    gen_launch_prompt = get_gen_launch_prompt()

    gen_launch_chain = LLMChain(
        llm=llm,
        prompt=gen_launch_prompt,
        verbose=verbose
    )

    gen_launch_output = gen_launch_chain.predict(task=task, node_topic_list=node_topic_list, project_name=project_name)

    to_files(gen_launch_output, project_name, 'launch')

    print(ui.GEN_LAUNCH_MSG)


def install_generator(task, node_topic_list, project_name, llm, verbose=False):
    gen_cmake_prompt = get_gen_cmake_prompt()

    gen_cmake_chain = LLMChain(
        llm=llm,
        prompt=gen_cmake_prompt,
        verbose=verbose
    )

    gen_cmake_output = gen_cmake_chain.predict(task=task, node_topic_list=node_topic_list, project_name=project_name)

    to_files(gen_cmake_output, project_name, 'install')

    gen_package_prompt = get_gen_package_prompt()

    gen_package_chain = LLMChain(
        llm=llm,
        prompt=gen_package_prompt,
        verbose=verbose
    )

    gen_package_output = gen_package_chain.predict(task=task, node_topic_list=node_topic_list,
                                                   project_name=project_name)

    to_files(gen_package_output, project_name, 'install')

    print(ui.GEN_INSTALL_MSG)


def to_files(chat, project_name, mode):
    workspace = dict()

    files = get_code_from_chat(chat)
    for file_name, code in files:
        if file_name == 'README.md':
            continue

        workspace[file_name] = code

    for filename in workspace.keys():
        code = workspace[filename]

        if mode == 'src':
            with open(f'catkin_ws/src/{project_name}/src/{filename}', 'w') as file:
                file.write(code)
        elif mode == 'launch':
            with open(f'catkin_ws/src/{project_name}/launch/{filename}', 'w') as file:
                file.write(code)
        elif mode == 'install':
            with open(f'catkin_ws/src/{project_name}/{filename}', 'w') as file:
                file.write(code)
        else:
            print('Invalid file storage mode!')
