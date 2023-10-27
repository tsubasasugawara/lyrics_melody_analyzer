import pprint
from alm.node import node as nd
from alm.comparator import extracting_subtree as es

def node_map_test():
    root = nd.Node(
        1,
        [
            nd.Node(
                2,
                [
                    nd.Node(
                        4,
                        [],
                        True,
                        3
                    ),
                    nd.Node(
                        5,
                        [],
                        True,
                        3
                    ),
                    nd.Node(
                        6,
                        [],
                        True,
                        3
                    ),
                ],
                False,
                2
            ),
            nd.Node(
                3,
                [
                    nd.Node(
                        7,
                        [],
                        True,
                        3
                    )
                ],
                False,
                2
            ),
        ],
        False,
        1
    )

    parent_child_list = es.extract_parent_child(root)

    node_map = nd.NodeMap(parent_child_list)
    node_map.parent_child_to_dict()
    root_ids = node_map.find_roots()

    for root_id in root_ids:
        tree = node_map.gen_tree(root_id, 1)
        pprint.pprint(tree.to_dict())

node_map_test()