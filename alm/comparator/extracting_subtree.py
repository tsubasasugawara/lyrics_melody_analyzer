def extract_subtree(tree: dict) -> list:
    node_id = tree["id"]
    
    res = []
    for child in tree["children"]:
        children = extract_subtree(child)
        res.append(join_subtree(children, child["id"]))
    
    return res

def join_subtree(subtree_list: list, node_id: int) -> list:
    length = len(subtree_list)
    res = []

    for i in range(2 ** length):
        node = {"id": node_id, "children": []}
        for j in range(length):
            if ((i >> j) & 1):
                node["children"].append(subtree_list[j])
        res.append(node)
    

    return res
