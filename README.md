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

**New in v0.0.4:**
ROScribe can now be used as your personal robotics consultant!

A vector database of all open-source ROS repositories available on [ROS Index](https://index.ros.org/) is built, and using retrieval augmented generation (RAG), ROScribe can answer every question regarding relevant ROS packages for your project. Chekout [this wiki](https://github.com/RoboCoachTechnologies/ROScribe/wiki/3.-Explore-ROS-Repositories-with-RAG) for more information.

## How to use

Please see our wiki page to learn how to install and use ROScribe in your robotics projects:
* [Installation](https://github.com/RoboCoachTechnologies/ROScribe/wiki/1.-Installation)
* [ROS Package Generation using ROScribe](https://github.com/RoboCoachTechnologies/ROScribe/wiki/2.-ROS-Package-Generation)
* [Explore Open-source Robotics Repositories using ROScribe-RAG](https://github.com/RoboCoachTechnologies/ROScribe/wiki/3.-Explore-ROS-Repositories-with-RAG)

## Demos

- [TurtleSim Code Generation with ROScribe](https://www.youtube.com/watch?v=H2QaeelkReU)
- [ROScribe-RAG Demo](https://www.youtube.com/watch?v=3b5FyZvlkxI&list=PLN8Hz7F2GjIkiYVForVuyvNs17sggQYOt&index=3)

## Roadmap

Currently, ROScribe only supports ROS1 with Python code generation. We aim to add the following features in the coming releases:
- ROS2 support
- C++ code generation
- ROS1 to ROS2 automated codebase migration

As an open-source project, we encourage all robotics enthusiasts to contribute to ROScribe. During each release, we will announce the list of new contributors.

## Contact

For business inquiries, such as consulting or contracting jobs, please contact robocoachtechnologies@gmail.com. 

