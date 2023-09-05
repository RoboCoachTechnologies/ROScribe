WELCOME_MSG = """
Welcome to ROScribe! I am here to assist you with creating a robot software.

First, please briefly tell me what you would like to implement. Don't worry about the details! We will talk about them later.
"""

NODE_MSG_ANALYZE_INIT = """
I am going to analyze our conversation and identify the ROS nodes and ROS topics that are going to be involved in our project.

Give me a few seconds!
"""

NODE_MSG_ANALYZE_FINISH = """
I finished my analysis! Based on my knowledge, you might need the following ROS nodes and ROS topics:
"""

SHOW_NODE_GRAPH = """
Do you want to see a node graph of your project?
"""

SHOW_NODE_GRAPH_AGAIN = """
Do you want to see the updated node graph of your project?
"""

YN_RESP_ERROR = """
Invalid answer. Please answer with only 'yes' or 'no'.
"""

CHECK_FOR_MOD_INIT = """
Would you like to add or remove any ROS nodes?
"""

CHECK_FOR_MOD_AGAIN = """
Would you like to add or remove additional ROS nodes?
"""

TRY_MOD_AGAIN = """
Would you like to try again?
"""

MOD_INST = """
In order to add a ROS node, provide a 4-tuple with the following format:

(
 'ROS_node_name',
 'ROS_node_description',
 [('subscribed_topic_1', 'ROS_message_type'), ('subscribed_topic_2', 'ROS_message_type'), ...],
 [('published_topic_1', 'ROS_message_type'), ('published_topic_2', 'ROS_message_type'), ...]
)

For removing a ROS node, you can follow the above format, but leave the node description empty. For example:

('node_name_to_be_removed', '', [], [])
"""

MOD_SUCCESS = """
Your list of ROS nodes have been successfully updated. Here is the new list:
"""

MOD_SUCCESS_W_WARN = """
Your list of ROS nodes have been successfully updated, but the following warning was found:

{warning_msg}

Here is the new list:
"""

MOD_FAILED = """
Update failed!

{warning_msg}
"""

QA_MSG_INIT = """
Now I am going to ask some questions about the details for each of the components. Your answers will help me to better understand the specifications of the problem you are working on.
"""

QA_MSG_TITLE = """
Let's talk about {node}.
"""

LAUNCH_INSTALL_MSG = """
It seems like we have implemented all the ROS nodes for the project. Now I am going to finalize the package creation by adding launch files, CMakeLists, and ROS package description.
"""

GEN_NODE_CODE_MSG = """
I finished the implementation for ROS node {node}! You can find it in the 'workspace' directory.
"""

GEN_LAUNCH_MSG = """
ROS launch file creation completed!
"""

GEN_INSTALL_MSG = """
CMakeLists.txt and package.xml files have been created!
"""

FAREWELL_MSG = """
Your ROS package implementation is complete!

Farewell my friend!
"""
