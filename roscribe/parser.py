import re, ast

from schema import Schema, SchemaError

from typing import List, Dict, Tuple

from pydantic import BaseModel, Field

from langchain.output_parsers import PydanticOutputParser


# Data structure for the output of ROS nodes
class NodeList(BaseModel):
    ros_nodes: Dict[str, str] = Field(description="dictionary containing ROS node names as keys and ROS node descriptions as values")


def get_node_parser():
    return PydanticOutputParser(pydantic_object=NodeList)


def make_node_list(node_list):
    node_list_str = ""
    for node in node_list.keys():
        node_list_str += "- " + node + ": " + node_list[node] + "\n"
    return node_list_str


# Data structure for the output of ROS topics
class TopicList(BaseModel):
    ros_topics: List[Tuple[str, str, List[str], List[str]]] = Field(description="list of 4-tuples where each 4-tuple stores ROS topic name as 1st element, ROS topic message type as 2nd element, list of publishing ROS nodes as 3rd element, and list of subscribing ROS nodes as 4th element.")


def get_topic_parser():
    return PydanticOutputParser(pydantic_object=TopicList)


def make_node_topic_dict(node_list, topic_list):
    node_topic_dict = dict()
    for node in node_list.keys():
        topic_pub_list = []
        topic_sub_list = []
        for topic in topic_list:
            if node in topic[2]:
                topic_pub_list.append((topic[0], topic[1]))
            if node in topic[3]:
                topic_sub_list.append((topic[0], topic[1]))

        node_topic_dict[node] = {'description': node_list[node],
                                 'published_topics': topic_pub_list,
                                 'subscribed_topics': topic_sub_list}

    return node_topic_dict


def make_node_topic_list_str(node_topic_dict):
    node_topic_list_str = ""
    for node in node_topic_dict.keys():
        if len(node_topic_dict[node]['subscribed_topics']) == 0:
            topic_sub_str = "No Subscribed Topics"
        else:
            topic_sub_str = ""
            for topic in node_topic_dict[node]['subscribed_topics']:
                topic_sub_str += "{topic_name} (message type: {topic_msg_type}), "\
                    .format(topic_name=topic[0], topic_msg_type=topic[1])

        if len(node_topic_dict[node]['published_topics']) == 0:
            topic_pub_str = "No Published Topics"
        else:
            topic_pub_str = ""
            for topic in node_topic_dict[node]['published_topics']:
                topic_pub_str += "{topic_name} (message type: {topic_msg_type}), "\
                    .format(topic_name=topic[0], topic_msg_type=topic[1])

        node_topic_list_str += "- " + node + ":\n" + \
                               "\t\tDescription: " + node_topic_dict[node]['description'] + "\n" + \
                               "\t\tSubscribed Topics: " + topic_sub_str + "\n" + \
                               "\t\tPublished Topics: " + topic_pub_str + "\n"

    return node_topic_list_str


MOD_INPUT_SCHEMA = Schema((str, str, [(str, str)], [(str, str)]))


def modify_node_dict(mod_input, node_topic_dict):
    try:
        mod_tuple = ast.literal_eval(mod_input)
    except SyntaxError:
        warning_msg = "Invalid input. Please make sure that your input only contains the list of modifications."
        return node_topic_dict, False, warning_msg

    try:
        MOD_INPUT_SCHEMA.validate(mod_tuple)
    except SchemaError as schema_error:
        warning_msg = "Invalid input. Please make sure that you follow the input format. Here is the generated error:\n\n"\
                      + str(schema_error)
        return node_topic_dict, False, warning_msg

    warning_msg = ""
    success = True
    if mod_tuple[1] == "":
        if mod_tuple[0] in node_topic_dict.keys():
            node_topic_dict.pop(mod_tuple[0])
        else:
            warning_msg += "Adding ROS node {node_name} failed due to empty node description."\
                .format(node_name=mod_tuple[0])
            success = False
    else:
        if len(mod_tuple[2]) == 0 and len(mod_tuple[3]) == 0:
            warning_msg += "ROS node {node_name} neither publishes nor subscribes to any topic!"\
                .format(node_name=mod_tuple[0])

        node_topic_dict[mod_tuple[0]] = {'description': mod_tuple[1],
                                         'subscribed_topics': mod_tuple[2],
                                         'published_topics': mod_tuple[3]}

    return node_topic_dict, success, warning_msg


def get_code_from_chat(chat):
    # Get all code blocks and preceding file names
    regex = r"(\S+)\n\s*```[^\n]*\n(.+?)```"
    matches = re.finditer(regex, chat, re.DOTALL)

    files = []
    for match in matches:
        # Strip the filename of any non-allowed characters
        path = re.sub(r'[<>"|?*]', "", match.group(1))

        # Remove leading and trailing brackets
        path = re.sub(r"^\[(.*)\]$", r"\1", path)

        # Remove leading and trailing backticks
        path = re.sub(r"^`(.*)`$", r"\1", path)

        # Remove trailing ]
        path = re.sub(r"\]$", "", path)

        # Get the code
        code = match.group(2)

        # Add the file to the list
        files.append((path, code))

    readme = chat.split("```")[0] + '\n' + chat.split("```")[-1]
    files.append(("README.md", readme))

    # Return the files
    return files
