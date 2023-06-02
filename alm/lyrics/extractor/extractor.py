import xml.etree.ElementTree as et

class Extractor:
    def __init__(self):
        """歌詞を抽出するためのクラス

        Attributes:
            part (str): パートのID
            chars (dict): 抽出し音符と対応付けた歌詞のリスト
        """
        self.part = ""
        self.lyrics_notes_map = {}

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

        self.part = tree.find("part").attrib["id"]
        self.__mapping_lyrics_notes(tree.iter("measure"))

    def __mapping_lyrics_notes(self, measures) -> None:
        """歌詞を抽出し、音符と対応付ける

        Args:
            #TODO: measureのタイプ
            measures (Any): xmlからiter関数によって抜き出したmeasureタグのリスト
        """
        
        lyric = ""
        for measure in measures:
            measure_number = measure.attrib["number"]
            self.lyrics_notes_map[measure_number] = {}
            
            notes_cnt = 0
            for note in measure.iter("note"):
                notes_cnt += 1

                if note.find("rest") != None:
                    continue

                lyric_ele = note.find("lyric")
                if lyric_ele != None:
                    lyric = lyric_ele.find("text").text
                    self.lyrics_notes_map[measure_number][lyric] = [notes_cnt]
                elif self.lyrics_notes_map[measure_number].get(lyric) == None:
                    self.lyrics_notes_map[measure_number][lyric] = [notes_cnt]
                else:
                    self.lyrics_notes_map[measure_number][lyric].append(notes_cnt)
                