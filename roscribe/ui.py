SPEC_AGENT_WELCOME_MSG = """
Welcome to ROScribe! I am here to assist you with creating a robot software.

As a first step, please briefly tell me what you would like to implement. Don't worry about the details! We will talk about them later.
"""


SPEC_AGENT_FAREWELL_MSG = """
It seems like we now have a high-level understanding of the ROS project. I am going to pass the information about the project to the generator agent.
"""


GEN_AGENT_WELCOME_MSG = """
Hey there! This is the generator agent! I am here to help you with implementing your ROS nodes.
"""


GEN_AGENT_NODE_MSG = """
Let's get started with implementing '{curr_node}'. Do you prefer to implement this node from scratch? or alternatively use an open-source project if possible?
"""


GEN_AGENT_FAREWELL_MSG = """
Now that we are done with writing the code for the ROS nodes, we need to create installation scripts and documentation for the project.

The packaging agent will take over this conversation to help you with the next steps.
"""


PACK_AGENT_LAUNCH_MSG = """
Hey there! This is the packaging agent! I am here to help you with finalizing your ROS project.

The following are the main steps to make sure your ROS project will be working smoothly:
1- Writing a ROS launch file to start the necessary ROS nodes.
2- Defining package.xml and CMakeLists.txt files so we can build your ROS package.
3- Creating a README.md file that contains information about your ROS package.

We start by writing a launch file. Based on the information provided by the generator package, I have prepared an initial launch file shown below:

{launch}

Let me know what changes you would like to make to this launch file.
"""


PACK_AGENT_PACKAGE_MSG = """
Now that we are done with writing the launch file, let's switch our focus on defining a package.xml file for our ROS package.

Based on the information provided by the generator package, I have prepared an initial package.xml file shown below:

{package}

Let me know what changes you would like to make to this package.xml file.
"""


PACK_AGENT_CMAKE_MSG = """
Now that we are done with writing the package.xml file, let's switch our focus on defining a CMakeLists.txt file for our ROS package.

Based on the information provided by the generator package, I have prepared an initial CMakeLists.txt file shown below:

{cmake}

Let me know what changes you would like to make to this CMakeLists.txt file.
"""


PACK_AGENT_README_MSG = """
Last but not least, let's create a README.md file for our ROS package.

Based on the information provided by the generator package, I have prepared an initial README.md file shown below:

{readme}

Let me know what changes you would like to make to this README.md file.
"""


PACK_AGENT_FAREWELL_MSG = """
The implementation of your ROS project has finished, congratulations!

I understand that there might be still some problems down the road. The support agent will help you for the rest of the project's life cycle in case you encountered any issues.
"""


SUPPORT_AGENT_LAUNCH_MSG = """
Hi there! This is the support agent. Feel free to ask me questions regarding your ROS project.

Keep in mind that I can internally read the generated files for the project, so you don't need to copy/paste them to the chat.
"""
