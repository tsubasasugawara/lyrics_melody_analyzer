import xml.etree.ElementTree as et
from ...utils import util

PART_KEY = "parts"
LYRICS_KEY = "lyrics"

class LyricsExtractor:
    def __init__(self):
        """歌詞をMusicXMLから抽出するためのクラス

        Attributes:
            part (str): パートのID
            lyrics_notes_map (dict): 抽出し音符と対応付けた歌詞のリスト
            lyrics (str): 歌詞
        """
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

        self.lyrics_notes_map[PART_KEY] = {}
        self.__mapping_lyrics_notes(tree.iter("measure"))

    def to_json(self, file_path: str) -> None:
        """抽出結果をJSONファイルとして出力する

        Args:
            file_path (str): 出力先ファイルのパス
        """

        util.output_json(file_path, self.lyrics_notes_map)

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
            measure_lyrics = ""
            self.lyrics_notes_map[PART_KEY][measure_number] = {LYRICS_KEY: "", "notes": {}}
            
            notes_cnt = 0
            for note in measure.iter("note"):
                notes_cnt += 1

                if note.find("rest") != None:
                    continue

                note_id = '-'.join([PART_KEY, measure_number, str(notes_cnt)])

                lyric_ele = note.find("lyric")
                if lyric_ele != None:
                    char= lyric_ele.find("text").text

                    measure_lyrics = measure_lyrics + char
                    lyrics = lyrics + char

                    self.lyrics_notes_map[PART_KEY][measure_number]["notes"][char] = [note_id]
                elif self.lyrics_notes_map[PART_KEY][measure_number]["notes"].get(char) == None:
                    self.lyrics_notes_map[PART_KEY][measure_number]["notes"][char] = [note_id]
                else:
                    self.lyrics_notes_map[PART_KEY][measure_number]["notes"][char].append(note_id)

                self.lyrics_notes_map[PART_KEY][measure_number][LYRICS_KEY] = measure_lyrics

        self.lyrics_notes_map[PART_KEY][LYRICS_KEY] = lyrics 
        self.lyrics = lyrics
