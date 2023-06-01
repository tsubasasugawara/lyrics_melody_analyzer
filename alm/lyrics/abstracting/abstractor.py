#TODO:ファイル名の変更
import xml.etree.ElementTree as et

class Abstractor:
    def __init__(self):
        """歌詞を抽出するためのクラス

        Attributes:
            part (str): パートのID
            chars (list): 抽出された歌詞のリスト
        """
        self.part = ""
        self.chars = []

    def abstract_lyrics(self, file_path: str):
        """MusicXmlから歌詞のみを抽出する

        Args:
            file_path (str): 歌詞を抽出したファイルのパス
        """

        try:
            tree = et.parse(file_path)
        except et.ParseError as err:
            print("ParseError:", err)
            return

        self.part = tree.iter("part").attrib["id"]

        # xmlから抽出した小節のリストから文字列を抜き出す
        for m in tree.iter("measure"):
            self.mapping_lyrics_notes_per_measure(m)

    def mapping_lyrics_notes_per_measure(ele: et.Element) -> None:
