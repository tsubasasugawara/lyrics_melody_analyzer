from alm.node import node as nd
import copy
import itertools

def extract_parent_child(node: nd.Node) -> list:
    res = []
    for child in node.children:
        res.append({"id": node.id, "child": child.id})
        res.extend(extract_parent_child(child))
    
    return res

def extract_parent_brothers(node: nd.Node) -> list:
    if node.end:
        return None

    res = []
    for i in range(1, 2**len(node.children)):
        res.append(nd.Node(node.id, [], False))
        for j in range(len(node.children)):
            if i >> j & 1:
                res[i-1].children.append(nd.Node(node.children[j].id, [], True))
    
    for child in node.children:
        child_subtree = extract_parent_brothers(child)
        if child_subtree != None:
            res.extend(child_subtree)

    return res

def extract_subtree(node: nd.Node, subtree_dict: map):
    subtree_dict[node.id] = []

    if node.end:
        return

    # 子ノードをルートとした部分木を子ノードごとに格納
    subtrees_lists = []
    for i in range(len(node.children)):
        extract_subtree(node.children[i], subtree_dict)
        subtrees_lists.append(copy.deepcopy(subtree_dict[node.children[i].id]))
        subtrees_lists[i].append(nd.Node(node.children[i].id, [], True))

    # subtrees_listからbit全探索を用いて全組み合わせの部分木の生成を行う
    for i in range(1, 2**len(subtrees_lists)):
        lists = []
        for j in range(len(subtrees_lists)):
            if i >> j & 1:
                lists.append(subtrees_lists[j])

        combinations = itertools.product(*lists)
        for ele in combinations:
            subtree_dict[node.id].append(nd.Node(node.id, list(ele), False))
   