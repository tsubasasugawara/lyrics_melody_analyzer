import spacy
from spacy import displacy
from ...utils import util

#TODO: LyricsExtractorで歌詞と対応付けた音符情報も保持させる
class GrammarParser:
    def __init__(self, nlp_model_name: str):
        """歌詞の文法構造を解析するクラス

        Args:
            nlp_model_name (str): 使用する自然言語処理モデル名
        
        Attribute:
            nlp (spacy.Language): モデルを読み込んだもの
            doc (spacy.Language): 文法解析の結果
            tree (dict): 文法構造の構文解析木
            words (list): 形態素解析で分割した単語のリスト
        """

        self.nlp = spacy.load(nlp_model_name)
        self.doc = None
        self.tree = None
        self.words = []

    def parse(self, lyrics: str) -> None:
        """歌詞の文法構造を解析する

        Args:
            lyrics (str): 解析したい歌詞
        """

        self.doc = self.nlp(lyrics)

        for token in self.doc:
            self.words.append(token.text)
    
    def to_tree_map(self) -> None:
        """係り受け木を辞書型にする
        """

        if self.doc == None:
            return

        tree_list = []
        for sent in self.doc.sents:
            tree_list.append(self.__recur_tree(sent.root))
        self.tree = self.__join_roots(tree_list)

    def __recur_tree(self, token) -> dict:
        """再帰的に木を作成する

        Args:
            token (_type_): 文法構造解析結果のトークン

        Returns:
            dict: ノード
        """
        node = {"word": token.text, "number": token.i, "children": {}}

        node["children"] = []
        for child in token.children:
            node["children"].append(self.__recur_tree(child))

        return node
    
    def __join_roots(self, roots: list) -> dict:
        """複数あるルートを一つにまとめる

        Args:
            roots (list): ルートのリスト

        Returns:
            dict: 結合後の木
        """

        if len(roots) <= 1:
            return roots

        res = roots[0]
        for i in range(1, len(roots)):
            if len(res["children"]) > len(roots[i]["children"]):
                temp = roots[i]
                temp["children"].append(res)
                res = temp
            else:
                res["children"].append(roots[i])

        return res
    
    def visualize(self) -> None:
        """歌詞の文法構造を可視化する
        """
        displacy.render(self.doc, style='dep', jupyter=True, options={"compact": True, "distance": 90})
