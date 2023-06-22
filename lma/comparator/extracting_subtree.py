def extract_subtree(tree: dict) -> list:
    parent_id = tree["id"]
    
    res = []
    for child in tree["children"]:
        child_id = child["id"]
        res.append({"parent": parent_id, "child": child_id})
        res.extend(extract_subtree(child))
    
    return res