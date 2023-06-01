import xml.etree.ElementTree as et
from . import node

def parse_time_span_tree(ts, parent):
    """タイムスパン木を解析し、Nodeによって木を構築する

    Args:
        ts (ElementTree): タイムスパン木のElementTree
        parent (Node): 親ノード
    """

    # primary要素
    primary = ts.find("./primary/ts")
    if primary != None:
        parse_time_span_tree(primary, parent)

    # secondary要素
    secondary = ts.find("./secondary/ts")
    if secondary != None:
        id = secondary.find("./head/chord/note").attrib["id"]
        sn = node.Node(id)
        parse_time_span_tree(secondary, sn)
        parent.children.append(sn)
    
def time_span_tree_to_json(file_path) -> node.Node:
    """タイムスパン木のXMLをJSONに変換する

    Args:
        file_path (str): XMLファイルのパス
    
    Returns:
        node.Node: タイムスパン木のルート

    Raises:
        ParseError:XMLの解析に失敗したときの例外
    """

    # XMLファイルを解析
    try:
        tree = et.parse(file_path)
    except et.ParseError as err:
        print("ParseError:", err)

    root = tree.getroot()
    #TODO: root.findで要素がなかったときの処理を追加
    head = node.Node(root.find("./ts/head/chord/note").attrib["id"])
    parse_time_span_tree(root.find("./ts"), head)

    return head