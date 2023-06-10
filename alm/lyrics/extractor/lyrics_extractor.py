import xml.etree.ElementTree as et
from ...utils import util

CHAR_NOTES_KEY = "char_notes"
MEASURES_KEY = "measures"
LYRICS_KEY = "lyrics"
CHAR_KEY = "char"
NOTES_KEY = "notes"
CHAR_NUMBER = "char_number"

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
        self.lyrics_notes_map = {CHAR_NOTES_KEY: [], MEASURES_KEY: [], LYRICS_KEY: ""}
        self.__mapping_lyrics_notes(tree.iter("measure"))

        self.__split_a_char()

    def to_json(self, file_path: str) -> None:
        """抽出結果をJSONファイルとして出力する

        Args:
            file_path (str): 出力先ファイルのパス
        """

        util.output_json(file_path, self.lyrics_notes_map)

    def __split_a_char(self) -> None:
        """一つの音符に2文字以上が対応しているときに分割する
        """

        index = 0
        while True:
            if index >= len(self.lyrics_notes_map[CHAR_NOTES_KEY]) - 1:
                break

            chars = self.lyrics_notes_map[CHAR_NOTES_KEY][index][CHAR_KEY]

            char_list = list(chars)
            if len(char_list) <= 1:
                index += 1
                continue

            char_notes = self.lyrics_notes_map[CHAR_NOTES_KEY][index]
            self.lyrics_notes_map[CHAR_NOTES_KEY].pop(index)
            for i in range(len(char_list)):
                self.lyrics_notes_map[CHAR_NOTES_KEY].insert(index + i, {CHAR_KEY: char_list[i], NOTES_KEY: char_notes[NOTES_KEY], CHAR_NUMBER: char_notes[CHAR_NUMBER]})

            index += len(char_list)

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
            notes_cnt = 0
            for note in measure.iter("note"):
                notes_cnt += 1

                if note.find("rest") != None:
                    continue

                note_id = '-'.join([self.part, measure_number, str(notes_cnt)])

                lyric_ele = note.find("lyric")
                if lyric_ele != None:
                    char= lyric_ele.find("text").text

                    measure_lyrics = measure_lyrics + char
                    lyrics = lyrics + char

                    self.lyrics_notes_map[CHAR_NOTES_KEY].append({CHAR_KEY: char, NOTES_KEY: [note_id]})
                    self.lyrics_notes_map[CHAR_NOTES_KEY][-1][CHAR_NUMBER] = len(self.lyrics_notes_map[CHAR_NOTES_KEY]) - 1
                else:
                    self.lyrics_notes_map[CHAR_NOTES_KEY][-1][NOTES_KEY].append(note_id)

            self.lyrics_notes_map[MEASURES_KEY].append(measure_lyrics)

        self.lyrics_notes_map[LYRICS_KEY] = lyrics 
        self.lyrics = lyrics
