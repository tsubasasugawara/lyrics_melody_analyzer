from alm.node import node as nd

def extract_parent_child(node: nd.Node) -> list:
    res = []
    for child in node.children:
        res.append({"id": node.id, "child": child.id})
        res.extend(extract_parent_child(child))
    
    return res

def extract_subtree(node: nd.Node):
    if node.end:
        return []
    
    res = []
    n = len(node.children)
    for i in range(1, 2**n):
        subtree = nd.Node(node.id, [], False)
        for j in range(n):
            if i >> j & 1:
                subtree.children.append(node.children[j])
        res.append(subtree)
    
    return res
