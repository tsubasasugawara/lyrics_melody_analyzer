import xml.etree.ElementTree as et
from alm.node import node

def time_span_tree_to_dict(file_path: str) -> node.Node:
    """タイムスパン木のXMLをJSONに変換する

    Args:
        file_path (str): XMLファイルのパス

    Returns:
        node.Node: タイムスパン木の辞書型配列
    
    Raises:
        ParseError:XMLの解析に失敗したときの例外
    """

    # XMLファイルを解析
    try:
        tree = et.parse(file_path)
    except et.ParseError as err:
        print("ParseError:", err)

    root = tree.getroot()
    head_id = root.find("./ts/head/chord/note").attrib["id"]
    if head_id == None:
        return
        
    head = node.Node(head_id, [])
    parse_time_span_tree(root.find("./ts"), head)

    return head

def parse_time_span_tree(ts: et.ElementTree, parent: node.Node):
    """タイムスパン木を解析し、Nodeによって木を構築する

    Args:
        ts (ElementTree): タイムスパン木のElementTree
        parent (node.Node): 親ノード
    """

    # primary要素
    primary = ts.find("./primary/ts")
    if primary != None:
        parse_time_span_tree(primary, parent)

    # secondary要素
    secondary = ts.find("./secondary/ts")
    if secondary != None:
        id = secondary.find("./head/chord/note").attrib["id"]
        sn = node.Node(id, [])
        parse_time_span_tree(secondary, sn)
        parent.children.append(sn)
    
    return parent
