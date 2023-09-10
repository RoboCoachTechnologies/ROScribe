# ROScribe

**Turn natural language into ROS packages with the power of LLMs.**

ROScribe helps you deploy robot software in the form of Robot Opertaing System (ROS) packages, only using human language input. Figure out your ROS nodes and topics, visualize the node graph, find the design specifications, and generate the code, all using ROScribe!

Inspired by [GPT Synthesizer](https://github.com/RoboCoachTechnologies/GPT-Synthesizer), ROScribe builds an entire ROS package through a series of specification steps that identify the package elements in a top-down approach. In particular, ROScribe helps you with the following steps:

1. Creating a list of ROS nodes and topics, based on your application and deployment (e.g. simulation vs. real-world)
2. Visualizing your project in an RQT-style graph
3. Generating code for each ROS node
4. Writing launch file and installation scripts

The natural language interface of ROScribe is intended to lower the skill barrier of using ROS for novice programmers, while still providing value to experienced ROS users. This is achieved thanks to the flexibility of large language models (LLMs) alongside the prompt tuning techniques of ROScribe.

If you are new to ROS, ROScribe will be your robot(ics) mentor 🤖️

If you are a seasoned ROS user, ROScribe can help with creating a blueprint for your ROS package 📦️

## Installation

- `pip install roscribe`

- For development:
  - `git clone https://github.com/RoboCoachTechnologies/ROScribe.git`
  - `cd ROScribe`
  - `pip install -e .`

## Usage

ROScribe uses OpenAI's `gpt-3.5-turbo-16k` as the default LLM. You can switch to other [supported models](https://python.langchain.com/docs/integrations/llms/) by LangChain; however you might have to get the API for each model or [run them locally](https://python.langchain.com/docs/integrations/llms/huggingface_pipelines).

- Setup your OpenAI API key: `export OPENAI_API_KEY=[your api key]`

**Run**:

- Start ROScribe by typing `roscibe` in the terminal.
- Briefly describe the robot software you want to deploy:
  - `Your Robot Software: I want to deploy 2-D occupancy grid mapping.`
- ROScibe will ask you high-level questions reagrding your deployment:
  - `ROScribe: Are you going to deploy your mapping algorithm on a real robot or use a dataset?`
  - `Answer: I am going to deploy my software on a robot with a 2-D LiDAR...`
- When ROScribe learns about your project, it will show you a list of ROS nodes and topics that will be involved in you software.
- The subscription/publisher relationship between the ROS nodes can be visualized similar to RQT graph.
- Moreover, you can edit the list of ROS nodes and topics based on your preference.
- After you finalize the node list, ROScribe will start identifying the specifications of each ROS node through a Q&A process. This is the most immportant step since the fial implmentation would be highly influenced by this conversation.
- The code for each node is generated when ROScribe finds all the implmentation details.
- Finally, a ROS launch file and installation scripts (package.xml and CMakeLists.txt) are created according to the project requirements.

## Roadmap

Currently, ROScribe only supports ROS1 with Python code generation. We aim to add the following features in the coming releases:
- ROS2 support
- C++ code generation
- ROS1 to ROS2 automated code-base migration

As an open-source project, we encourage all robotics enthusiasts to contribute to ROScribe. During each release, we will announce the list of new contributors.

## Contact

For business inquiries, such as consulting or contracting jobs, please contact robocoachtechnologies@gmail.com. 

