# ROScribe

**Turn natural language into ROS packages with the power of LLMs.**

ROScribe helps you deploy robot software in the form of Robot Opertaing System (ROS) packages, only using human language input. Figure out your ROS nodes and topics, visualize the node graph, find the design specifications, and generate the code, all using ROScribe!

Inspired by [GPT Synthesizer](https://github.com/RoboCoachTechnologies/GPT-Synthesizer), ROScribe builds an entire ROS package through a series of specification steps that identify the package elements in a top-down approach. In particular, ROScribe helps you with the following steps:

1. Creating a list of ROS nodes and topics, based on your application and deployment (e.g. simulation vs. real-world)
2. Visualizing your project in a RQT-style graph
3. Generating code for each ROS node
4. Writing launch file and installation scripts

## Installation

- `pip install roscribe`

- For development:
  - `git clone https://github.com/RoboCoachTechnologies/ROScribe.git`
  - `cd ROScribe`
  - `pip install -e .`

## Usage

ROScribe uses OpenAI's `gpt-3.5-turbo-16k` as the default LLM.

- Setup your OpenAI API key: `export OPENAI_API_KEY=[your api key]`

**Run**:

- Start ROScribe by typing `roscibe` in the terminal.

## Roadmap



## Contact

For business inquiries, such as consulting or contracting jobs, please contact robocoachtechnologies@gmail.com. 

