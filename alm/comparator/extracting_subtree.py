from alm.node import node as nd
import copy
from alm.utils import math
import itertools

PARENT_CHILD_COMBINATIONS = "parent_child_combinations"

def extract_parent_child(node: nd.Node) -> list:
    res = []
    for child in node.children:
        res.append({"id": node.id, "child": child.id})
        res.extend(extract_parent_child(child))
    
    return res

def count_subtree(node: nd.Node, count_subtree_map: dict):
    if node.end:
        count_subtree_map[node.id] = 0
        return
    
    for child in node.children:
        count_subtree(child, count_subtree_map)

    count_subtree_map[node.id] = 0
    for k in range(len(node.children)):
        count_subtree_map[node.id] += math.comb(len(node.children), k)
    
    if PARENT_CHILD_COMBINATIONS not in count_subtree_map:
        count_subtree_map[PARENT_CHILD_COMBINATIONS] = count_subtree_map[node.id]
    elif node.depth > 1:
        count_subtree_map[PARENT_CHILD_COMBINATIONS] += count_subtree_map[node.id]

    for i in range(1, 2**len(node.children)):
        count = 1
        for j in range(len(node.children)):
            if i >> j & 1:
                count *= count_subtree_map[node.children[j].id]
        count_subtree_map[node.id] += count
    
    if node.depth == 1:
        count_subtree_map[node.id] += count_subtree_map[PARENT_CHILD_COMBINATIONS]
    
def extract_subtree(node: nd.Node, subtree_dict: map):
    subtree_dict[node.id] = []

    if node.end:
        return

    # 子ノードをルートとした部分木を子ノードごとに格納
    subtrees_lists = []
    for i in range(len(node.children)):
        extract_subtree(node.children[i], subtree_dict)
        subtrees_lists.append(copy.deepcopy(subtree_dict[node.children[i].id]))
        subtrees_lists[i].append(nd.Node(node.children[i].id, [], True, node.children[i].depth))

    # subtrees_listからbit全探索を用いて全組み合わせの部分木の生成を行う
    for i in range(1, 2**len(subtrees_lists)):
        lists = []
        for j in range(len(subtrees_lists)):
            if i >> j & 1:
                lists.append(subtrees_lists[j])

        combinations = itertools.product(*lists)
        for ele in combinations:
            subtree_dict[node.id].append(nd.Node(node.id, list(ele), False, node.depth))
   