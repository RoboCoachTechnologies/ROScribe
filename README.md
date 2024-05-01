# ROScribe

**Create ROS packages using LLMs.**

Using a natural language interface to describe robotic projects, ROScribe eliminates the skill barrier of using ROS for beginners, and saves time and hassle for skilled engineers. ROScribe combines the sheer power and flexibility of large language models (LLMs) with prompt tuning techniques to capture the details of your robotic design and to automatically create an entire ROS package for your project.

ROScribe builds an entire ROS workspace via an agentic multi-step approach, where each step focuses on one specific aspect of robot software design. In particular, ROScribe helps you with the following steps:

1. Identify and visualize a list of ROS nodes and topics, based on the application and deployment (e.g. simulation vs. real-world)
2. Generate code or pull from open-source repositories for each ROS node.
3. Integrate the code base over the generated and open-source assets.
4. User support throughout the life-cycle of the project.

If you are new to ROS, ROScribe will be your robot(ics) mentor 🤖️

If you are a seasoned ROS user, ROScribe can help with creating a blueprint for your ROS package 📦️

## How to use

ROScribe is composed of 4 agents. The list below details the responsibilities of each agent, shown in the order of interaction:
1. `SpecAgent`: Helps with the overall skeleton of your project. In ROS terms, it builds the ROS graph of your project, where each part of the graph can be either AI-generated or pulled from an open-source reository.
2. `GenAgent`: Given the ROS graph, this agent generates the ROS workspace and the code for each ROS node in python. Alternatively, it can download an open-source implementation for the ROS node.
3. `PackAgent`: With the knowledge of the generated ROS workspace, this agent creates a ROS launch file that brings up the ROS nodes. Furthermore, `package.xml`, `CMakeLists.txt`, and `README.md` files are generated by this agent.
4. `SupportAgent`: This is your customer support agent, which can help you whenever you encountered an error during running your project. The agent already has access to the layout of the project, and can internally read the generated files.

The following figure illustrates the architecture of ROScribe:
![](https://github.com/RoboCoachTechnologies/ROScribe/blob/master/docs/roscribe_arch.png)

Please see our wiki page to learn how to install and use ROScribe in your robotics projects:
* [Installation](https://github.com/RoboCoachTechnologies/ROScribe/wiki/1.-Installation)
* [Running ROScribe](https://github.com/RoboCoachTechnologies/ROScribe/wiki/2.-Running-ROScribe)
* [Create Your Own ROS Index Database](https://github.com/RoboCoachTechnologies/ROScribe/wiki/3.-Create-Your-Own-ROS-Index-Database)

## Demos

- [LiDAR Simultaneous Localization and Mapping (SLAM)](https://www.youtube.com/watch?v=iIIxcBJARDQ)

## Additional documentations & articles

[Looking inside ROScribe and the idea of LLM-based robotic platform](https://discourse.ros.org/t/looking-inside-roscribe-and-the-idea-of-llm-based-robotic-platform/34298) 

[Presentation slides of UCSD ROS workshop Oct. 27, 2023](docs/assets/ROScribeDeepDive.pdf)

[Video recording of UCSD ROS workshop presentation Oct. 27, 2023](https://www.youtube.com/watch?v=CPHleR-3Wko)

## Contact

For business inquiries, such as consulting or contracting jobs, please contact robocoachtechnologies@gmail.com.

As an open-source project, we encourage all robotics enthusiasts to contribute to ROScribe. During each release, we will announce the list of new contributors.
