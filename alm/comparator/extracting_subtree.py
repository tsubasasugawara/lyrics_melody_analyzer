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

    # 親と子のすべての組み合わせを抽出する
    for i in range(1, 2**len(node.children)):
        subtree = nd.Node(node.id, [], False)
        for j in range(len(node.children)):
            if i >> j & 1:
                subtree.children.append(nd.Node(node.children[j].id, [], True))
        subtree_dict[node.id].append(subtree)

    if left_len == 0 and right_len > 0:
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
                ]
            )
    elif left_len > 0 and right_len == 0:
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
                ]
            )
    elif left_len > 0 and right_len > 0:
        for left_subtree in left_subtrees:
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
