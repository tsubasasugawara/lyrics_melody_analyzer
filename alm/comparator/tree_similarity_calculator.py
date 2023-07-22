from alm.comparator import *
from alm.lyrics import *
from alm.melody import *

class TreeSimilarity:
    def __init__(self, denominator: int, numerator: int) -> None:
        """木の類似度計算の結果を入れるクラス

        Args:
            denominator (int): 分母
            numerator (int): 分子
        """

        self.denominator = denominator
        self.numerator = numerator

    def calc_similarity(self) -> float:
        """類似度を計算する

        Returns:
            float: 類似度
        """

        return self.numerator / self.denominator

def calc_tree_similarity(mscx_path: str, tstree_path: str) -> TreeSimilarity:
    """木の類似度を計算する

    Args:
        mscx_path (str): MusicXMLのパス
        tstree_path (str): タイムスパン木のパス

    Returns:
        _type_: _description_
    """
    lyrics_notes_map = lyrics_extractor.extract_lyrics(mscx_path)

    parser = grammar_parser.GrammarParser("ja_ginza")
    doc = parser.parse(lyrics_notes_map[lyrics_extractor.LYRICS_KEY])
    lyrics_tree = parser.to_tree(doc)

    words_notes_map = {}
    associating_lyrics_melody.explore_words_in_tree(lyrics_tree, words_notes_map)
    words_list = associating_lyrics_melody.associate_word_list_notes(words_notes_map, lyrics_notes_map)

    tstree = time_span_tree.tstree_xml_2_struct(tstree_path)
    notes_word_map = associating_lyrics_melody.associate_notes_words(words_list)
    
    associating_lyrics_melody.associate_tstree_words(tstree, notes_word_map)
    associating_lyrics_melody.associate_words_tree_notes(lyrics_tree, words_notes_map)

    lyrics_subtree_list = extracting_subtree.extract_parent_child(lyrics_tree)
    ts_subtree_list = extracting_subtree.extract_parent_child(tstree)

    cnt = 0
    for lyrics_subtree in lyrics_subtree_list:
        for ts_subtree in ts_subtree_list:
            if lyrics_subtree["id"] == ts_subtree["id"] and lyrics_subtree["child"] == ts_subtree["child"]:
                cnt += 1

    tree_similarity = TreeSimilarity(max(len(lyrics_subtree_list), len(ts_subtree_list)), cnt)
    return tree_similarity
