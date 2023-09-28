from alm.node import node as nd

def extract_parent_child(node: nd.Node) -> list:
    res = []
    for child in node.children:
        res.append({"id": node.id, "child": child.id})
        res.extend(extract_parent_child(child))
    
    return res

def connect_tree(parent_id, left: nd.Node, right: nd.Node, subtree_dict: map):
    res = []
    for lsubtree in subtree_dict[left.id]:
        for rsubtree in subtree_dict[right.id]:
           res.append(nd.Node(parent_id, [lsubtree, rsubtree], False)) 
    return res

def extract_subtree(node: nd.Node, subtree_dict: map):
    if node.end:
        return []

    left_subtrees = extract_subtree(node.children[0], subtree_dict)
    right_subtrees = extract_subtree(node.children[1], subtree_dict)

    left_len = len(left_subtrees)
    right_len = len(right_subtrees)

    subtree_dict[node.id] = []

    if left_len == 0 and right_len == 0:
        subtree_dict[node.id] = [
            nd.Node(
                node.id,
                [node.children[0], node.children[1]],
                False
                ),
            nd.Node(
                node.id,
                [node.children[0]],
                False
                ),
            nd.Node(
                node.id,
                [node.children[1]],
                False
                ),
            ]
    elif left_len == 0:
        for right_subtree in right_subtrees:
            subtree_dict[node.id].extend(
                [
                    nd.Node(
                        node.id,
                        [node.children[0], right_subtree],
                        False
                    ),
                    nd.Node(
                        node.id,
                        [right_subtree],
                        False
                    ),
                    nd.Node(
                        node.id,
                        [node.children[0]],
                        False
                    )
                ]
            )
    elif right_len == 0:
        for left_subtree in left_subtrees:
            subtree_dict[node.id].extend(
                [
                    nd.Node(
                        node.id,
                        [left_subtree, node.children[1]],
                        False
                    ),
                    nd.Node(
                        node.id,
                        [left_subtree],
                        False
                    ),
                    nd.Node(
                        node.id,
                        [node.children[1]],
                        False
                    ),
                ]
            )
    else:
        for left_subtree in lefft_subtrees:
            for right_subtree in right_subtrees:
                subtree_dict[node.id].extend(
                    [
                        nd.Node(
                            node.id,
                            [left_subtree, right_subtree],
                            False
                        ),
                        nd.Node(
                            node.id,
                            [left_subtree],
                            False
                        ),
                        nd.Node(
                            node.id,
                            [right_subtree],
                            False
                        ),
                    ]
                )
    
    return subtree_dict[node.id]

# def extract_subtree(node: nd.Node, subtree_dict: map) -> (list, bool):
#     if node.end:
#         return []

#     res = []
#     n = len(node.children)
#     for i in range(1, 2**n):
#         subtree = nd.Node(node.id, [], False)
#         for j in range(n):
#             if i >> j & 1:
#                 subtree.children.append(node.children[j])
#         res.append(subtree)
    
#     return res
