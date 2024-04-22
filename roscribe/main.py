from roscribe.spec_agent import SpecAgent, load_spec_agent
from roscribe.gen_agent import GenAgent, load_gen_agent
from roscribe.pack_agent import PackAgent, load_pack_agent
from roscribe.support_agent import SupportAgent


def main(verbose=False):
    verbose = False

    spec_agent = SpecAgent(ros_distro='noetic', verbose=verbose)
    spec_agent.spin()
    loaded_spec_agent = load_spec_agent('spec_agent.pkl')
    gen_agent = GenAgent(ros_distro='noetic', ros_graph_dict=loaded_spec_agent.get_ros_graph_dict(),
                         ros_node_desc=loaded_spec_agent.get_ros_node_desc(), verbose=verbose)
    gen_agent.spin()
    loaded_gen_agent = load_gen_agent('gen_agent.pkl', 'spec_agent.pkl')
    pack_agent = PackAgent(ros_distro='noetic', ros_graph_dict=loaded_spec_agent.get_ros_graph_dict(),
                           ros_node_desc=loaded_spec_agent.get_ros_node_desc(), ros_nodes=loaded_gen_agent.nodes,
                           project_name=loaded_gen_agent.project_name, ws_name=loaded_gen_agent.ws_name,
                           verbose=verbose)
    pack_agent.spin()
    loaded_pack_agent = load_pack_agent('pack_agent.pkl', 'gen_agent.pkl', 'spec_agent.pkl')
    support_agent = SupportAgent(ros_distro='noetic', ros_graph_dict=loaded_spec_agent.get_ros_graph_dict(),
                                 ros_nodes=loaded_gen_agent.nodes, project_name=loaded_gen_agent.project_name,
                                 ws_name=loaded_gen_agent.ws_name, dependencies=loaded_pack_agent.dependencies,
                                 package=loaded_pack_agent.package, verbose=verbose)
    support_agent.spin()


if __name__ == '__main__':
    main()

