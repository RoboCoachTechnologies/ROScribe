import graphviz as gv


def show_node_graph(node_topic_dict):
    graph = gv.Digraph()
    graph.attr(rankdir='LR')

    topic_list = []

    for node in node_topic_dict.keys():
        graph.node(node, style ='solid', color='black', shape='ellipse')

        for sub_topic in node_topic_dict[node]['subscribed_topics']:
            if sub_topic[0] not in topic_list:
                topic_list.append(sub_topic[0])
                graph.node(sub_topic[0], style='solid', color='black', shape='box')
            graph.edge(sub_topic[0], node)

        for pub_topic in node_topic_dict[node]['published_topics']:
            if pub_topic[0] not in topic_list:
                topic_list.append(pub_topic[0])
                graph.node(pub_topic[0], style='solid', color='black', shape='box')
            graph.edge(node, pub_topic[0])

    graph.view()


def test_node_graph():
    node_topic_dict = {'node_A': {'description': 'node_A description',
                                  'published_topics': [('topic_1', 'topic_1_msg_type'), ('topic_2', 'topic_2_msg_type')],
                                  'subscribed_topics': [('topic_3', 'topic_3_msg_type')]},
                       'node_B': {'description': 'node_B description',
                                  'published_topics': [('topic_3', 'topic_3_msg_type')],
                                  'subscribed_topics': []},
                       'node_C': {'description': 'node_C description',
                                  'published_topics': [('topic_2', 'topic_2_msg_type')],
                                  'subscribed_topics': [('topic_1', 'topic_1_msg_type')]},
                       }

    show_node_graph(node_topic_dict)


if __name__ == '__main__':
    test_node_graph()
