from alm.node import node as nd
import copy

def extract_parent_child(node: nd.Node) -> list:
    res = []
    for child in node.children:
        res.append({"id": node.id, "child": child.id})
        res.extend(extract_parent_child(child))
    
    return res

def extract_subtree(node: nd.Node, subtree_dict: map):
    if node.end:
        return []

    left_subtrees = extract_subtree(node.children[0], subtree_dict)
    right_subtrees = extract_subtree(node.children[1], subtree_dict)

    left_subtrees.append(nd.Node(node.children[0].id, [], False))
    right_subtrees.append(nd.Node(node.children[1].id, [], False))

    subtree_dict[node.id] = []

    for right_subtree in right_subtrees:
        subtree_dict[node.id].append(
            nd.Node(
                    node.id,
                    [right_subtree],
                    False
                )
            )

    for left_subtree in left_subtrees:
        subtree_dict[node.id].append(
            nd.Node(
                    node.id,
                    [left_subtree],
                    False
                )
            )

    for left_subtree in left_subtrees:
        for right_subtree in right_subtrees:
            subtree_dict[node.id].append(
                    nd.Node(
                        node.id,
                        [left_subtree, right_subtree],
                        False
                    )
            )
    
    return copy.deepcopy(subtree_dict[node.id])
