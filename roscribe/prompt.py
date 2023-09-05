from langchain.prompts.prompt import PromptTemplate
from roscribe.parser import get_node_parser, get_topic_parser


def get_project_name_prompt():
    template = """The following is a description of a programming task that needs to be implemented in ROS, which stands for Robot Operating System.
    
    - Task description: {task}
    
    Choose a short name for this task to be used as the ROS package name.
    
    Obey the ROS package name conventions when choosing the name.
    
    The name should be in lower case only.
    
    Your output should be only the name without any other text before or after the name.
    """
    return PromptTemplate(template=template, input_variables=["task"])


def get_task_spec_prompt(task):
    template = """A human wants to write a robotics software with the help of a super talented software engineer AI.
    
    The AI is very proficient in robotics, especially in writing robot software in ROS, which stands for Robot Operating System.
    
    The human task is provided below:
    - Human task: {task}
    
    The human wants the task to be implemented in ROS1 using Python programming language.
    
    The AI's role here is to help the human to identify the specifications for implementing the task.
    
    Since the task is a robotics project, the AI should make sure all the robotics-related aspects of the project are clarified.
    For example, the AI should ask questions regarding:
    - Whether or not the human task is going to be deployed on a real robot.
    - If the human task is going to be deployed on a real robot, what are the hardware specifications of the robot? For example, what type of processors, sensors, and actuators the robot has?
    - If the human task is going to be used on a dataset, ask about the details of the dataset.
    
    The AI uses the following conversation in order to design questions that identify the specifications for implementing the human task.

    The AI will continue asking questions until all robotics-related aspects of the human task become clear. The AI will stop asking questions when it thinks there is no need for further clarification about the human task.
    
    The conversation should remain high-level and in the context of robotics and the human task. There is no need to provide code snippets.
    
    The AI should not generate messages on behalf of the human. The AI should ask one question at a time. The AI concludes the conversation by saying 'END_OF_TASK_SPEC'.

    Current conversation:
    {history}
    Human: {input}
    AI:"""
    return PromptTemplate(template=template,
                          input_variables=["history", "input"],
                          partial_variables={"task": task}), "END_OF_TASK_SPEC"


def get_task_spec_summarize_prompt():
    template = """The following is a conversation between an AI and a human regarding implementation of a robot software.
    
    Summarize the conversation in bullet point format by extracting the most important information exchanged within the conversation.
    
    Please include any mentioned numbers in the summary, as they are important to the conversation.

    Conversation:
    {input}"""
    return PromptTemplate(template=template, input_variables=["input"])


def get_gen_node_prompt():
    template = """A human wants to write a robotics software with the help of a super talented software engineer AI.
    
    The AI is very proficient in robotics, especially in writing robot software in ROS, which stands for Robot Operating System.
    
    The human task is provided below:
    - Human task: {task}
    
    The human wants the task to be implemented in ROS1 using Python programming language.
    
    The AI's role here is to help the human to identify the components for implementing the task.
    
    In particular, the AI should generate a dictionary containing the ROS nodes that are required to implement the task using ROS.
    
    The AI should consider the following summary as a reference for the specifications of the human task:
    {summary}
    
    The AI generates the ROS node names and ROS node descriptions as a dictionary, where the names are dictionary keys and the descriptions are dictionary values.

    {format_instructions}
    
    The AI does not need to provide code snippets. Each identified ROS node should be responsible for a part of the task.

    The ROS nodes should be complementary to each other, and their description should indicate how each ROS node is used by the other ROS nodes."""
    parser = get_node_parser()
    return PromptTemplate(template=template, input_variables=["task", "summary"],
                          partial_variables={"format_instructions": parser.get_format_instructions()}), parser


def get_gen_topic_prompt():
    template = """A human wants to write a robotics software with the help of a super talented software engineer AI.

        The AI is very proficient in robotics, especially in writing robot software in ROS, which stands for Robot Operating System.

        The human task is provided below:
        - Human task: {task}

        The human wants the task to be implemented in ROS1 using Python programming language.

        The AI's role here is to help the human to identify the components for implementing the task.

        The AI takes a list of the ROS nodes that are involved in the implementation of the task.
        Using the node list, the AI generates a list containing the ROS topics that are needed for communication between the ROS nodes.

        The AI should consider the following summary as a reference for the specifications of the human task:
        {summary}

        Here is the list of ROS nodes that are involved in the task:
        {ros_nodes}
        
        The AI generates the list of ROS topics as a list of 4-tuples, with the following properties:
        1. The first element of the tuple contains the ROS topic name.
        2. The second element of the tuple contains the message type of the ROS topic.
        3. The third element of the tuple contains the list of ROS nodes that publish this ROS topic. This list can be empty by default.
        4. The forth element of the tuple contains the list of ROS nodes that subscribe to this ROS topic. This list can be empty by default.

        {format_instructions}

        The AI does not need to provide code snippets. Each identified ROS topic should be responsible for connecting a subset of ROS nodes."""
    parser = get_topic_parser()
    return PromptTemplate(template=template, input_variables=["task", "summary", "ros_nodes"],
                          partial_variables={"format_instructions": parser.get_format_instructions()}), parser


def get_node_qa_prompt(task, node_topic_list, curr_node):
    template = """A human wants to write a robotics software with the help of a super talented software engineer AI.
    
    The AI is very proficient in robotics, especially in writing robot software in ROS, which stands for Robot Operating System.
    
    The human task is provided below:
    - Human task: {task}
    
    The human wants the task to be implemented in ROS1 using Python programming language.
    
    The AI has identified the following list of ROS nodes that need to be implemented for the task:
    {node_topic_list}
    
    Currently, the AI needs to only focus on the ROS node named '{curr_node}' for the task. The other components in the list above are just provided for context.
    
    The AI uses the following conversation in order to design questions that identify the specifications for implementing '{curr_node}' in particular.
    
    The AI should avoid asking redundant questions that can be already answered using the information provided in the description of '{curr_node}'.

    The AI will continue asking questions until all the details for implementing '{curr_node}' become clear. The AI will stop asking questions when it thinks there is no need for further clarification about '{curr_node}'.

    The conversation should remain high-level and in the context of robotics and the human task. There is no need to provide code snippets.
    
    The AI should not generate messages on behalf of the human. The AI should ask one question at a time. The AI concludes the conversation by saying 'END_OF_NODE_SPEC'.

    Current conversation:
    {history}
    Human: {input}
    AI:"""
    return PromptTemplate(template=template,
                          input_variables=["history", "input"],
                          partial_variables={"task": task,
                                             "node_topic_list": node_topic_list,
                                             "curr_node": curr_node}), "END_OF_NODE_SPEC"


def get_node_qa_sum_prompt():
    template = """The following is a conversation between an AI and a human regarding implementation of a robot software.

    Summarize the conversation in bullet point format by extracting the most important information exchanged within the conversation.

    Please include any mentioned numbers in the summary, as they are important to the conversation.

    Conversation:
    {input}"""
    return PromptTemplate(template=template, input_variables=["input"])


def get_gen_code_prompt():
    template = """You are a super talented software engineer AI.
    
    In particular, You are very proficient in robotics, especially in writing robot software in ROS, which stands for Robot Operating System.
    
    A human wants to write a robotics software with your help.
    
    The human task is provided below:
    - Human task: {task} 
    
    The human wants the task to be implemented in ROS1 using Python programming language.
    
    Here is the list of ROS nodes that need to be implemented for the task:
    {node_topic_list}
    
    Your sole focus is implementing the ROS node named '{curr_node}' for the task. The above information is purely provided for context so that you know how your implementation of '{curr_node}' plays a role within the task.
    
    For additional information, here is a summary of a conversation between the human and another AI to further clarify how the human would like the code for '{curr_node}' to be implemented.
    
    Summary:
    {summary}
    
    Implement the ROS node '{curr_node}' in Python programming language using ROS1. Make sure that you fully implement everything that is necessary for the code to work.
    Think step by step and reason yourself to the right decisions to make sure we get it right.

    Output your implementation strictly in the following format.

    FILENAME
    ```python
    CODE
    ```

    Where 'CODE' is your implementation and 'FILENAME' is '{curr_node}' formatted to a valid file name.

    Before you finish, double check to ensure your implementation of '{curr_node}' satisfies the following:
    - The code should be fully functional.
    - No placeholders are allowed.
    - Ensure to implement all code, if you are unsure, write a plausible implementation.
    - Your implementation satisfies all of the specifications mentioned in the above summary.
    - Your implementation takes into consideration all the topics that '{curr_node}' publishes or subscribes to."""
    return PromptTemplate(template=template,
                          input_variables=["task", "node_topic_list", "curr_node", "summary"])


def get_gen_launch_prompt():
    template = """You are a super talented software engineer AI.

    In particular, You are very proficient in robotics, especially in writing robot software in ROS, which stands for Robot Operating System.

    A human wants to write a robotics software with your help.

    The human task is provided below:
    - Human task: {task}
    - ROS package name: {project_name}

    The human wants the task to be implemented in ROS1.

    Here is the list of ROS nodes that has been implemented for the task:
    {node_topic_list}
    
    Your sole focus is to create a ROS launch file that launches the above ROS nodes, so that the user can start the task by calling the created launch file.
    
    Keep in mind that all of the ROS nodes are implemented in Python programming language.
    
    Also pay attention that the ROS package name is '{project_name}'.
    
    Make sure that you fully implement everything in the launch file that is necessary for the code to work.
    
    Think step by step and reason yourself to the right decisions to make sure we get it right.

    Output your created launch file strictly in the following format.

    FILENAME
    ```XML
    CODE
    ```

    Where 'CODE' is your created ROS launch script and 'FILENAME' is a valid ROS launch file name based on the task."""
    return PromptTemplate(template=template,
                          input_variables=["task", "node_topic_list", "project_name"])


def get_gen_cmake_prompt():
    template = """You are a super talented software engineer AI.

    In particular, You are very proficient in robotics, especially in writing robot software in ROS, which stands for Robot Operating System.

    A human wants to write a robotics software with your help.

    The human task is provided below:
    - Human task: {task}
    - Catkin package name: {project_name}

    The human wants the task to be implemented in ROS1 and built via catkin.

    Here is the list of ROS nodes that has been implemented for the task:
    {node_topic_list}

    Your sole focus is to create a CMakeLists file that contains the catkin installation directives.

    Keep in mind that all of the ROS nodes are implemented in Python programming language, so they don't need to be compiled.
    
    Also note that the catkin package name is '{project_name}'.

    In terms of dependencies, pay attention to the ROS message types in the list above; since the message types dictate the package dependencies.

    Make sure that you fully implement everything in the CMakeLists file that is necessary for the catkin installation to work.

    Think step by step and reason yourself to the right decisions to make sure we get it right.

    Output your created CMakeLists file strictly in the following format.

    CMakeLists.txt
    ```CMake
    CODE
    ```

    Where 'CODE' is your created CMakeLists script."""
    return PromptTemplate(template=template,
                          input_variables=["task", "node_topic_list"])


def get_gen_package_prompt():
    template = """You are a super talented software engineer AI.

    In particular, You are very proficient in robotics, especially in writing robot software in ROS, which stands for Robot Operating System.

    A human wants to write a robotics software with your help.

    The human task is provided below:
    - Human task: {task}
    - ROS package name: {project_name}

    The human wants the task to be implemented in ROS1.

    Here is the list of ROS nodes that has been implemented for the task:
    {node_topic_list}

    Your sole focus is to create a package.xml file that defines properties about the package such as the package name, version numbers, authors, maintainers, and dependencies on other catkin packages.

    In terms of dependencies, pay attention to the ROS message types in the list above; since the message types dictate the package dependencies.
    
    Also note that the ROS package name is '{project_name}'.

    Make sure that you fully implement everything in the package.xml file that is necessary for the catkin installation to work.

    Think step by step and reason yourself to the right decisions to make sure we get it right.

    Output your created package.xml file strictly in the following format.

    package.xml
    ```XML
    CODE
    ```

    Where 'CODE' is your created package.xml script."""
    return PromptTemplate(template=template,
                          input_variables=["task", "node_topic_list"])
