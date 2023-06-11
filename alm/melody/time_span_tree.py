import xml.etree.ElementTree as et
from ..utils import util

class TimeSpanTree:
    def __init__(self) -> None:
        """タイムスパン木の処理を行うクラス

        Attribute:
            time_span_tree_dict (dict): タイムスパン木を辞書型配列にしたもの
        """
        self.time_span_tree_dict = {}
    
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

    def time_span_tree_to_dict(self, file_path: str) -> None:
        """タイムスパン木のXMLをJSONに変換する

        Args:
            file_path (str): XMLファイルのパス
        
        Raises:
            ParseError:XMLの解析に失敗したときの例外
        """

        # XMLファイルを解析
        try:
            tree = et.parse(file_path)
        except et.ParseError as err:
            print("ParseError:", err)

        root = tree.getroot()
        head = self.Node(root.find("./ts/head/chord/note").attrib["id"])
        if head == None:
            return
        self.__parse_time_span_tree(root.find("./ts"), head)

        self.time_span_tree_dict = head.to_dict()

    def to_json(self, file_path: str) -> None:
        """タイムスパン木のJSONファイルを出力する

        Args:
            file_path (str): 出力先のファイルのパス
        """
        util.output_json(file_path, self.time_span_tree_dict)

    def __parse_time_span_tree(self, ts: et.ElementTree, parent: Node):
        """タイムスパン木を解析し、Nodeによって木を構築する

        Args:
            ts (ElementTree): タイムスパン木のElementTree
            parent (Node): 親ノード
        """

        # primary要素
        primary = ts.find("./primary/ts")
        if primary != None:
            self.__parse_time_span_tree(primary, parent)

        # secondary要素
        secondary = ts.find("./secondary/ts")
        if secondary != None:
            id = secondary.find("./head/chord/note").attrib["id"]
            sn = self.Node(id)
            self.__parse_time_span_tree(secondary, sn)
            parent.children.append(sn)
    
