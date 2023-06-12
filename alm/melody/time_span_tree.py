import xml.etree.ElementTree as et

class Node:
    """タイムスパン木のノード

    Attributes:
        id(str): 音符のID
        children(Node): 子ノード
    """
    def __init__(self, id):
        self.id = id
        self.children = []

    def to_dict(self) -> dict:
        """Nodeオブジェクトを辞書型配列にする

        Args:
            depth (int): 現在の深さ

        Returns:
            dict: Nodeを辞書型配列に変換した結果
        """

        res = {"id": self.id, "children": []}
        for child in self.children:
            res["children"].append(child.to_dict())

        return res 

def time_span_tree_to_dict(file_path: str) -> dict:
    """タイムスパン木のXMLをJSONに変換する

    Args:
        file_path (str): XMLファイルのパス

    Returns:
        dict: タイムスパン木の辞書型配列
    
    Raises:
        ParseError:XMLの解析に失敗したときの例外
    """

    # XMLファイルを解析
    try:
        tree = et.parse(file_path)
    except et.ParseError as err:
        print("ParseError:", err)

    root = tree.getroot()
    head = Node(root.find("./ts/head/chord/note").attrib["id"])
    if head == None:
        return
    __parse_time_span_tree(root.find("./ts"), head)

    return head.to_dict()

def __parse_time_span_tree(ts: et.ElementTree, parent: Node):
    """タイムスパン木を解析し、Nodeによって木を構築する

    Args:
        ts (ElementTree): タイムスパン木のElementTree
        parent (Node): 親ノード
    """

    # primary要素
    primary = ts.find("./primary/ts")
    if primary != None:
        __parse_time_span_tree(primary, parent)

    # secondary要素
    secondary = ts.find("./secondary/ts")
    if secondary != None:
        id = secondary.find("./head/chord/note").attrib["id"]
        sn = Node(id)
        __parse_time_span_tree(secondary, sn)
        parent.children.append(sn)
    
