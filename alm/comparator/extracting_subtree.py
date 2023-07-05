from alm.node import node

def extract_parent_child(node: node.Node) -> list:
    res = []
    for child in node.children:
        res.append({"id": node.id, "child": child.id})
        res.extend(extract_parent_child(child))
    
    return res


def join_subtree(subtree_list: list, node_id: int) -> list:
    n = len(subtree_list)
    res = []

    for bit in range(1 << (n)):
        node = {"id": node_id, "children": []}
        for i in range(n):
            if bit & (1 << i):
                node["children"].append(subtree_list[i])
        res.append(node)

    return res
