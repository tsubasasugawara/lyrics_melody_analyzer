from ..lyrics.extractor import lyrics_extractor as LE

class LyricsMelodyMatcher:
    def __init__(self, lyrics_tree: dict, lyrics_notes_map: dict):
        """歌詞とメロディを対応付けるクラス

        Args:
            lyrics_tree (dict): GrammarParserクラスで出力された歌詞の木
            lyrics_notes_map (dict): LyricsExtractorクラスで出力された音符と歌詞の対応を示したリスト

        Attribute:
            lyrics_tree (dict): GrammarParserクラスで出力された歌詞の木
            lyrics_notes_map (dict): LyricsExtractorクラスで出力された音符と歌詞の対応を示したリスト
            words_notes_map (dict): 単語ごとに音符と対応付けされたマップ
        """

        self.lyrics_tree = lyrics_tree
        self.lyrics_notes_map = lyrics_notes_map
        self.words_notes_map = {}

        self.__explore_words_in_tree(self.lyrics_tree)

    def __explore_words_in_tree(self, tree: dict) -> None:
        """構文解析木から単語を探索し、単語リストを作成する

        Args:
            tree (dict): 構文解析木の部分木
        """

        word = tree["word"]
        number = tree["number"]

        self.words_notes_map[number] = {"word": word, "notes": []}

        for child in tree["children"]:
            self.__explore_words_in_tree(child)

    def match_words_notes(self) -> None:
        """単語と音符を対応付ける
        """

        key_list = sorted(self.words_notes_map)
        index_words_map_key_list = 0

        chars = ""
        notes = []
        for index_lyrics_map in range(0, len(self.lyrics_notes_map[LE.CHAR_NOTES_KEY])):
            if index_words_map_key_list >= len(key_list):
                break

            key = key_list[index_words_map_key_list]
            word = self.words_notes_map[key]["word"]

            chars = chars + self.lyrics_notes_map[LE.CHAR_NOTES_KEY][index_lyrics_map][LE.CHAR_KEY]
            notes.extend(self.lyrics_notes_map[LE.CHAR_NOTES_KEY][index_lyrics_map][LE.NOTES_KEY])

            if word == chars:
                self.words_notes_map[key]["notes"] = notes
                index_words_map_key_list += 1

                notes = []
                chars = ""
