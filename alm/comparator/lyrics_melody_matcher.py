class LyricsMelodyMatcher:
    def __init__(self, lyrics_tree: dict, lyrics_words: list, lyrics_notes_map: dict, melody_tree:dict):
        """歌詞とメロディを対応付けるクラス

        Args:
            lyrics_tree (dict): GrammarParserクラスで出力された歌詞の木
            lyrics_words (list): 形態素解析によって分割した単語のリスト
            lyrics_notes_map (dic): LyricsExtractorクラスで出力された音符と歌詞の対応を示したリスト
            melody_tree (dict): メロディの木
        """

        self.lyrics_tree = lyrics_tree
        self.lyrics_words = lyrics_words
        self.lyrics_notes_map = lyrics_notes_map
        self.melody_tree = melody_tree
