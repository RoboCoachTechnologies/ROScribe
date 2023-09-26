import os

from langchain.chains import LLMChain

from roscribe.prompt import get_gen_code_prompt, get_gen_launch_prompt,\
    get_gen_cmake_prompt, get_gen_package_prompt
from roscribe.parser import get_code_from_chat

import roscribe.ui as ui


ROS_WS_NAME = 'ros_ws'

SETUP_PY_TEMPLATE = """
setup.py
```python
from setuptools import setup

package_name = '{package_name}'

setup(
 name=package_name,
 version='0.0.1',
 packages=[package_name],
 data_files=[
     ('share/ament_index/resource_index/packages',
             ['resource/' + package_name]),
     ('share/' + package_name, ['package.xml']),
   ],
 install_requires=['setuptools'],
 zip_safe=True,
 maintainer='TODO',
 maintainer_email='TODO',
 description='TODO: Package description',
 license='TODO: License declaration',
 tests_require=['pytest'],
 entry_points={console_scripts},
)
```
"""


SETUP_CFG_TEMPLATE = """
setup.cfg
```cfg
[develop]
script_dir=$base/lib/{package_name}
[install]
install_scripts=$base/lib/{package_name}
```
"""


def make_setup_py(node_topic_dict, package_name):
    console_scripts = "'console_scripts': ["
    for node in node_topic_dict.keys():
        console_scripts += f"'{node} = {package_name}.{node}:main', "

    console_scripts = console_scripts[:-2] + "]"

    setup_py = SETUP_PY_TEMPLATE.format(package_name=package_name, console_scripts=console_scripts)
    return setup_py


def make_setup_cfg(package_name):
    setup_cfg = SETUP_CFG_TEMPLATE.format(package_name=package_name)
    return setup_cfg


def ros_ws_generator(project_name, ros_version):
    if not os.path.exists(ROS_WS_NAME):
        os.mkdir(ROS_WS_NAME)

    if not os.path.exists(f'{ROS_WS_NAME}/src'):
        os.mkdir(f'{ROS_WS_NAME}/src')

    os.mkdir(f'{ROS_WS_NAME}/src/{project_name}')
    os.mkdir(f'{ROS_WS_NAME}/src/{project_name}/launch')

    if ros_version == 'ros1':
        os.mkdir(f'{ROS_WS_NAME}/src/{project_name}/src')
    elif ros_version == 'ros2':
        os.mkdir(f'{ROS_WS_NAME}/src/{project_name}/{project_name}')
        open(f'{ROS_WS_NAME}/src/{project_name}/{project_name}/__init__.py', 'x')

        os.mkdir(f'{ROS_WS_NAME}/src/{project_name}/resource')
        open(f'{ROS_WS_NAME}/src/{project_name}/resource/{project_name}', 'x')


def code_generator(task, node_topic_list, curr_node, summary, project_name, ros_version, llm, verbose=False):
    gen_code_prompt = get_gen_code_prompt(ros_version)

    gen_code_chain = LLMChain(
        llm=llm,
        prompt=gen_code_prompt,
        verbose=verbose
    )

    gen_code_output = gen_code_chain.predict(task=task, node_topic_list=node_topic_list,
                                             curr_node=curr_node, summary=summary)

    to_files(gen_code_output, project_name, 'impl', ros_version)

    print(ui.GEN_NODE_CODE_MSG.format(node=curr_node))


def launch_generator(task, node_topic_list, project_name, ros_version, llm, verbose=False):
    gen_launch_prompt = get_gen_launch_prompt(ros_version)

    gen_launch_chain = LLMChain(
        llm=llm,
        prompt=gen_launch_prompt,
        verbose=verbose
    )

    gen_launch_output = gen_launch_chain.predict(task=task, node_topic_list=node_topic_list, project_name=project_name)

    to_files(gen_launch_output, project_name, 'launch')

    print(ui.GEN_LAUNCH_MSG)


def install_generator(task, node_topic_dict, node_topic_list, project_name, ros_version, llm, verbose=False):
    if ros_version == 'ros1':
        gen_cmake_prompt = get_gen_cmake_prompt()

        gen_cmake_chain = LLMChain(
            llm=llm,
            prompt=gen_cmake_prompt,
            verbose=verbose
        )

        gen_cmake_output = gen_cmake_chain.predict(task=task, node_topic_list=node_topic_list,
                                                     project_name=project_name)
        to_files(gen_cmake_output, project_name, 'install')

    elif ros_version == 'ros2':
        setup_py = make_setup_py(node_topic_dict, project_name)
        to_files(setup_py, project_name, 'install')

        setup_cfg = make_setup_cfg(project_name)
        to_files(setup_cfg, project_name, 'install')

    gen_package_prompt = get_gen_package_prompt(ros_version)

    gen_package_chain = LLMChain(
        llm=llm,
        prompt=gen_package_prompt,
        verbose=verbose
    )

    gen_package_output = gen_package_chain.predict(task=task, node_topic_list=node_topic_list,
                                                   project_name=project_name)

    to_files(gen_package_output, project_name, 'install')

    print(ui.GEN_INSTALL_MSG)


def to_files(chat, project_name, mode, ros_version='ros1'):
    workspace = dict()

    files = get_code_from_chat(chat)
    for file_name, code in files:
        if file_name == 'README.md':
            continue

        workspace[file_name] = code

    for filename in workspace.keys():
        code = workspace[filename]

        if mode == 'impl':
            if ros_version == 'ros1':
                with open(f'{ROS_WS_NAME}/src/{project_name}/src/{filename}', 'w') as file:
                    file.write(code)
            elif ros_version == 'ros2':
                with open(f'{ROS_WS_NAME}/src/{project_name}/{project_name}/{filename}', 'w') as file:
                    file.write(code)

        elif mode == 'launch':
            with open(f'{ROS_WS_NAME}/src/{project_name}/launch/{filename}', 'w') as file:
                file.write(code)

        elif mode == 'install':
            with open(f'{ROS_WS_NAME}/src/{project_name}/{filename}', 'w') as file:
                file.write(code)
        else:
            print('Invalid file storage mode!')


def test_setup_py():
    package_name = 'my_package'
    node_topic_dict = {'node_A': {'description': 'node_A description',
                                  'published_topics': [('topic_1', 'topic_1_msg_type'),
                                                       ('topic_2', 'topic_2_msg_type')],
                                  'subscribed_topics': [('topic_3', 'topic_3_msg_type')]},
                       'node_B': {'description': 'node_B description',
                                  'published_topics': [('topic_3', 'topic_3_msg_type')],
                                  'subscribed_topics': []},
                       'node_C': {'description': 'node_C description',
                                  'published_topics': [('topic_2', 'topic_2_msg_type')],
                                  'subscribed_topics': [('topic_1', 'topic_1_msg_type')]},
                       }
    print(make_setup_py(node_topic_dict, package_name))


def test_setup_cfg():
    package_name = 'my_package'
    print(make_setup_cfg(package_name))


def test_dump_setup():
    package_name = 'my_package'
    node_topic_dict = {'node_A': {'description': 'node_A description',
                                  'published_topics': [('topic_1', 'topic_1_msg_type'),
                                                       ('topic_2', 'topic_2_msg_type')],
                                  'subscribed_topics': [('topic_3', 'topic_3_msg_type')]},
                       'node_B': {'description': 'node_B description',
                                  'published_topics': [('topic_3', 'topic_3_msg_type')],
                                  'subscribed_topics': []},
                       'node_C': {'description': 'node_C description',
                                  'published_topics': [('topic_2', 'topic_2_msg_type')],
                                  'subscribed_topics': [('topic_1', 'topic_1_msg_type')]}
                       }

    ros_ws_generator(package_name, 'ros2')

    setup_py = make_setup_py(node_topic_dict, package_name)
    to_files(setup_py, package_name, 'install')

    setup_cfg = make_setup_cfg(package_name)
    to_files(setup_cfg, package_name, 'install')


if __name__ == '__main__':
    test_setup_py()
    test_setup_cfg()
    test_dump_setup()
