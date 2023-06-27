def extract_subtree(tree: dict) -> list:
    node_id = tree["id"]

    return join_subtree(tree["children"], node_id)

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
