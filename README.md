# ROScribe

**Create ROS packages using LLMs.**

Using a natural language interface to describe robotic projects, ROScribe eliminates the skill barrier of using ROS for beginners, and saves time and hassle for skilled engineers. ROScribe combines the sheer power and flexibility of large language models (LLMs) with prompt tuning techniques to capture the details of your robotic design and to automatically create an entire ROS package for your project.

Inspired by [GPT Synthesizer](https://github.com/RoboCoachTechnologies/GPT-Synthesizer), ROScribe builds an entire ROS package through a series of specification steps that identify the package elements in a top-down approach. In particular, ROScribe helps you with the following steps:

1. Creating a list of ROS nodes and topics, based on your application and deployment (e.g. simulation vs. real-world)
2. Visualizing your project in an RQT-style graph
3. Generating code for each ROS node
4. Writing launch file and installation scripts

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

- Start ROScribe by typing `roscribe` in the terminal.

https://github.com/RoboCoachTechnologies/ROScribe/assets/85717407/5473d8f7-8701-4d4c-aa42-9bb87280b8d7

- Briefly describe the robot software you want to deploy.

https://github.com/RoboCoachTechnologies/ROScribe/assets/85717407/e1382d14-71f8-4985-9c0b-a09b8ce052f8

- ROScibe asks you high-level questions regarding your deployment.

https://github.com/RoboCoachTechnologies/ROScribe/assets/85717407/27113957-64c2-45b8-ac83-b437b3c88c9c

- Once ROScribe learns about your project, it shows you a list of ROS nodes and topics that are involved in your software. The subscriber/publisher relationship between the ROS nodes can be visualized similar to RQT graph.

https://github.com/RoboCoachTechnologies/ROScribe/assets/85717407/35819068-a724-4b8c-baa2-3aa1ca35f84d

- Moreover, you can edit (i.e. add/remove) the list of ROS nodes and topics based on your preference.

https://github.com/RoboCoachTechnologies/ROScribe/assets/85717407/0c05c637-9cc4-4289-8703-c156492fe247

- After you finalize the node list, ROScribe will start identifying the specifications of each ROS node through a Q&A process. This is the most important step since the final implementation would be highly influenced by this conversation.

https://github.com/RoboCoachTechnologies/ROScribe/assets/85717407/f99687f2-745d-47c5-916f-b9b16a8c86a3

- The code for each node is generated when ROScribe finds all the implementation details. Additionally, ROS launch file and installation scripts (package.xml and CMakeLists.txt) are created according to the project requirements. For Python ROS nodes, don't forget to allow executing your nodes as programs via `chmod +x ros_node.py`.

https://github.com/RoboCoachTechnologies/ROScribe/assets/85717407/eadf8815-44e4-4713-9c1d-c94886562a2b

- After ROScribe finishes code generation, you can install your ROS package by using `catkin`. After installation, source your workspace in order to link to your ROS packages.

https://github.com/RoboCoachTechnologies/ROScribe/assets/85717407/af893a3a-e9d8-4a4a-b490-ce799c069fe9

- You can launch your ROS package by using `roslaunch` command and calling the generated launch file.

https://github.com/RoboCoachTechnologies/ROScribe/assets/85717407/9850ed36-a834-45a6-a6ae-22362baddec3

## Roadmap

Currently, ROScribe only supports ROS1 with Python code generation. We aim to add the following features in the coming releases:
- ROS2 support
- C++ code generation
- ROS1 to ROS2 automated codebase migration

As an open-source project, we encourage all robotics enthusiasts to contribute to ROScribe. During each release, we will announce the list of new contributors.

## Contact

For business inquiries, such as consulting or contracting jobs, please contact robocoachtechnologies@gmail.com. 

