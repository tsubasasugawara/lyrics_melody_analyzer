from alm.node import node

def extract_parent_child(node: node.Node) -> list:
    res = []
    for child in node.children:
        res.append({"id": node.id, "child": child.id})
        res.extend(extract_parent_child(child))
    
    return res

