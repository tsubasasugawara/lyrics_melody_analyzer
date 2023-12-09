class Node:
    def __init__(self, id, children: list, end: bool, depth: int, word: str =None, note_id: str=None, notes: str =None):
        """ノード

        Args:
            id (Any): ノードのID
            children (list): 子ノードのリスト
            end(bool): 葉かどうか
            depth (int): 深さ
            word (str, optional): 単語 Defaults to None.
            note_id (str, optional): 音符のID Defaults to None.
            notes (list, optional): 音符のリスト Defaults to None.
        """
        self.id = id
        self.word = word
        self.note_id = note_id
        self.depth = depth
        self.end = end
        self.notes = notes
        self.children = children

    def to_dict(self) -> dict:
        """Nodeオブジェクトを辞書型配列にする

        Returns:
            dict: Nodeを辞書型配列に変換した結果
        """

        res = {"id": self.id, "end": self.end, "children": [], "depth": self.depth}

        if self.word != None:
            res["word"] = self.word
        
        if self.note_id != None:
            res["note_id"] = self.note_id

        if self.notes != None:
            res["notes"] = self.notes

        for child in self.children:
            res["children"].append(child.to_dict())

        return res 

class ParentChildSubtree:
    def __init__(self, id: int, child_id: int, depth):
        self.id = id
        self.child_id = child_id
        self.depth = depth

class NodeMapElement:
    def __init__(self, parent_id: int, id: int, children: list = []):
        self.parent_id = parent_id
        self.id = id
        self.children = children

class NodeMap:
    def __init__(self, parent_child: list):
        self.parent_child = parent_child
        self.parent_child_map = {}
    
    def parent_child_to_dict(self):
        for ele in self.parent_child:
            if ele.id not in self.parent_child_map:
                self.parent_child_map[ele.id] = NodeMapElement(-1, ele.id, [ele.child_id])
            else:
                self.parent_child_map[ele.id].children.append(ele.child_id)

            if ele.child_id not in self.parent_child_map:
                self.parent_child_map[ele.child_id] = NodeMapElement(ele.id, ele.child_id, [])
            elif self.parent_child_map[ele.child_id].parent_id == -1:
                self.parent_child_map[ele.child_id].parent_id = ele.id
    
    def find_roots(self) -> list:
        roots = []
        for value in self.parent_child_map.values():
            if value.parent_id == -1:
                roots.append(value.id)
        return roots
    
    def gen_tree(self, node_id: int, depth: int) -> Node:
        node = Node(self.parent_child_map[node_id].id, [], False, depth)
        if len(self.parent_child_map[node_id].children) == 0:
            node.end = True
            return node
        
        for child_id in self.parent_child_map[node_id].children:
            node.children.append(self.gen_tree(child_id, depth+1))
        
        return node