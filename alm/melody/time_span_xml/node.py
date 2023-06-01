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
