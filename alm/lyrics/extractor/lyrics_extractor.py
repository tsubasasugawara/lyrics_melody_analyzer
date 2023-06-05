import xml.etree.ElementTree as et
from ...utils import util

class LyricsExtractor:
    def __init__(self):
        """歌詞をMusicXMLから抽出するためのクラス

        Attributes:
            part (str): パートのID
            lyrics_notes_map (dict): 抽出し音符と対応付けた歌詞のリスト
            lyrics (str): 歌詞
        """
        self.part = ""
        self.lyrics_notes_map = {}
        self.lyrics = ""

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
        self.lyrics_notes_map[self.part] = {}
        self.__mapping_lyrics_notes(tree.iter("measure"))

    def __mapping_lyrics_notes(self, measures) -> None:
        """歌詞を抽出し、音符と対応付ける

        Args:
            #TODO: measureのタイプ
            measures (Any): xmlからiter関数によって抜き出したmeasureタグのリスト
        """
        
        char= ''
        lyrics = ""
        for measure in measures:
            measure_number = measure.attrib["number"]
            self.lyrics_notes_map[self.part][measure_number] = {}
            
            notes_cnt = 0
            for note in measure.iter("note"):
                notes_cnt += 1

                if note.find("rest") != None:
                    continue

                note_id = '-'.join([self.part, measure_number, str(notes_cnt)])

                lyric_ele = note.find("lyric")
                if lyric_ele != None:
                    char= lyric_ele.find("text").text
                    lyrics = lyrics + char
                    self.lyrics_notes_map[self.part][measure_number][char] = [note_id]
                elif self.lyrics_notes_map[self.part][measure_number].get(char) == None:
                    self.lyrics_notes_map[self.part][measure_number][char] = [note_id]
                else:
                    self.lyrics_notes_map[self.part][measure_number][char].append(note_id)

        self.lyrics_notes_map[self.part][measure_number]["lyrics"] = lyrics 