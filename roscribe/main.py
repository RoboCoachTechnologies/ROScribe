from langchain.chains import ConversationChain, LLMChain
from langchain.memory import ConversationBufferMemory

from roscribe.model import llm_init
from roscribe.prompt import get_project_name_prompt, get_task_spec_prompt, get_task_spec_summarize_prompt,\
    get_gen_node_prompt, get_gen_topic_prompt, get_node_qa_prompt, get_node_qa_sum_prompt
from roscribe.parser import make_node_list, make_node_topic_dict, make_node_topic_list_str, modify_node_dict
from roscribe.generator import catkin_ws_generator, code_generator, launch_generator, install_generator
from roscribe.visualization import show_node_graph

import roscribe.ui as ui


def main(verbose=False):
    llm = llm_init()

    print(ui.WELCOME_MSG)

    task_message = input("Your Robot Software: ")  # User-specified task

    project_name_prompt = get_project_name_prompt()
    project_name_chain = LLMChain(
        llm=llm,
        prompt=project_name_prompt,
        verbose=verbose)
    project_name = project_name_chain.predict(task=task_message)

    catkin_ws_generator(project_name)

    task_spec_prompt, task_spec_end_str = get_task_spec_prompt(task_message)
    task_spec_memory = ConversationBufferMemory()
    task_spec_chain = ConversationChain(
        llm=llm,
        prompt=task_spec_prompt,
        memory=task_spec_memory,
        verbose=verbose)

    init_human_input = task_message
    task_spec_output = task_spec_chain.predict(input=init_human_input)

    print(task_spec_output)

    while task_spec_end_str not in task_spec_output:
        human_response = input("Answer: ")
        task_spec_output = task_spec_chain.predict(input=human_response)
        spec_output_clean = task_spec_output.replace(task_spec_end_str, "")
        print(spec_output_clean)

    print(ui.NODE_MSG_ANALYZE_INIT)

    task_spec_sum_prompt = get_task_spec_summarize_prompt()
    task_spec_summary_chain = LLMChain(
        llm=llm,
        prompt=task_spec_sum_prompt,
        verbose=verbose)

    task_spec_memory.return_messages = True
    task_spec_sum_output = task_spec_summary_chain.predict(input=task_spec_memory.load_memory_variables({}))

    node_gen_prompt, node_gen_parser = get_gen_node_prompt()
    node_gen_chain = LLMChain(
        llm=llm,
        prompt=node_gen_prompt,
        verbose=verbose)

    node_gen_output = node_gen_chain.predict(task=task_message, summary=task_spec_sum_output)
    node_gen_list = node_gen_parser.parse(node_gen_output).ros_nodes
    node_list_str = make_node_list(node_gen_list)

    topic_gen_prompt, topic_gen_parser = get_gen_topic_prompt()
    topic_gen_chain = LLMChain(
        llm=llm,
        prompt=topic_gen_prompt,
        verbose=verbose)

    topic_gen_output = topic_gen_chain.predict(task=task_message, summary=task_spec_sum_output, ros_nodes=node_list_str)
    topic_gen_list = topic_gen_parser.parse(topic_gen_output).ros_topics

    node_topic_dict = make_node_topic_dict(node_gen_list, topic_gen_list)
    node_topic_list_str = make_node_topic_list_str(node_topic_dict)

    print(ui.NODE_MSG_ANALYZE_FINISH)
    print(node_topic_list_str)

    print(ui.SHOW_NODE_GRAPH)
    human_response_graph = input("Answer (yes/no): ").lower()
    while human_response_graph not in ['yes', 'no']:
        print(ui.YN_RESP_ERROR)
        human_response_graph = input("Answer (yes/no): ").lower()

    if human_response_graph == 'yes':
        show_node_graph(node_topic_dict)

    print(ui.CHECK_FOR_MOD_INIT)
    human_response_mod = input("Answer (yes/no): ").lower()
    while human_response_mod not in ['yes', 'no']:
        print(ui.YN_RESP_ERROR)
        human_response_mod = input("Answer (yes/no): ").lower()

    while human_response_mod == 'yes':
        print(ui.MOD_INST)
        node_dict_mod = input("Your Modifications: ")
        node_topic_dict, success, warning_msg = modify_node_dict(node_dict_mod, node_topic_dict)

        if success:
            node_topic_list_str = make_node_topic_list_str(node_topic_dict)

            if warning_msg == "":
                print(ui.MOD_SUCCESS)
            else:
                print(ui.MOD_SUCCESS_W_WARN.format(warning_msg=warning_msg))
            print(node_topic_list_str)

            print(ui.SHOW_NODE_GRAPH_AGAIN)
            human_response_graph = input("Answer (yes/no): ").lower()
            while human_response_graph not in ['yes', 'no']:
                print(ui.YN_RESP_ERROR)
                human_response_graph = input("Answer (yes/no): ").lower()

            if human_response_graph == 'yes':
                show_node_graph(node_topic_dict)

            print(ui.CHECK_FOR_MOD_AGAIN)

        else:
            print(ui.MOD_FAILED.format(warning_msg=warning_msg))
            print(ui.TRY_MOD_AGAIN)

        human_response_mod = input("Answer (yes/no): ").lower()
        while human_response_mod not in ['yes', 'no']:
            print(ui.YN_RESP_ERROR)
            human_response_mod = input("Answer (yes/no): ").lower()

    print(ui.QA_MSG_INIT)

    for node in node_topic_dict.keys():
        node_spec_prompt, node_spec_end_str = get_node_qa_prompt(
            task=task_message, node_topic_list=node_topic_list_str, curr_node=node)
        node_spec_memory = ConversationBufferMemory()
        node_spec_chain = ConversationChain(
            llm=llm,
            prompt=node_spec_prompt,
            memory=node_spec_memory,
            verbose=verbose)

        init_human_input = "I want to implement ROS node '{node}'".format(node=node)
        node_spec_output = node_spec_chain.predict(input=init_human_input)

        print(ui.QA_MSG_TITLE.format(node=node))
        print(node_spec_output)

        while node_spec_end_str not in node_spec_output:
            human_response = input("Answer: ")
            node_spec_output = node_spec_chain.predict(input=human_response)
            node_spec_output_clean = node_spec_output.replace(node_spec_end_str, "")
            print(node_spec_output_clean)

        sum_prompt = get_node_qa_sum_prompt()
        summary_chain = LLMChain(
            llm=llm,
            prompt=sum_prompt,
            verbose=verbose
        )

        node_spec_memory.return_messages = True
        sum_output = summary_chain.predict(input=node_spec_memory.load_memory_variables({}))

        code_generator(task_message, node_topic_list_str, node, sum_output, project_name, llm, verbose)

    print(ui.LAUNCH_INSTALL_MSG)

    launch_generator(task_message, node_topic_list_str, project_name, llm)

    install_generator(task_message, node_topic_list_str, project_name, llm)

    print(ui.FAREWELL_MSG)


if __name__ == "__main__":
    main()
