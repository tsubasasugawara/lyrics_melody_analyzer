from alm.comparator import *
from alm.lyrics import *
from alm.melody import *
from alm.utils import io

class TreeSimilarity:
    def __init__(self, denominator: int, numerator: int, section_name: str) -> None:
        """木の類似度計算の結果を入れるクラス

        Args:
            denominator (int): 分母
            numerator (int): 分子
            section_name (str): 楽曲名とセクション。<楽曲名>_[A,S]
        """

        self.denominator = denominator
        self.numerator = numerator
        self.section_name = section_name

    def calc_similarity(self) -> float:
        """類似度を計算する

        Returns:
            float: 類似度
        """

        return self.numerator / self.denominator

def calc_tree_similarity(mscx_path: str, tstree_path: str, parser: grammar_parser.GrammarParser) -> TreeSimilarity:
    """木の類似度を計算する

    Args:
        mscx_path (str): MusicXMLのパス
        tstree_path (str): タイムスパン木のパス

    Returns:
        _type_: _description_
    """
    lyrics_notes_dict = lyrics_extractor.extract_lyrics(mscx_path)

    doc = parser.parse(lyrics_notes_dict[lyrics_extractor.LYRICS_KEY])
    lyrics_tree = parser.to_tree(doc)

    words_notes_dict = {}
    associating_lyrics_melody.explore_words_in_tree(lyrics_tree, words_notes_dict)
    words_list = associating_lyrics_melody.associate_word_list_notes(words_notes_dict, lyrics_notes_dict)

    tstree = time_span_tree.tstree_xml_2_struct(tstree_path)
    notes_word_dict = associating_lyrics_melody.associate_notes_words(words_list)
    
    associating_lyrics_melody.associate_tstree_words(tstree, notes_word_dict)
    associating_lyrics_melody.associate_words_tree_notes(lyrics_tree, words_notes_dict)

    lyrics_subtree_list = extracting_subtree.extract_parent_child(lyrics_tree)
    ts_subtree_list = extracting_subtree.extract_parent_child(tstree)

    cnt = 0
    for lyrics_subtree in lyrics_subtree_list:
        for ts_subtree in ts_subtree_list:
            if lyrics_subtree["id"] == ts_subtree["id"] and lyrics_subtree["child"] == ts_subtree["child"]:
                cnt += 1

    tree_similarity = TreeSimilarity(max(len(lyrics_subtree_list), len(ts_subtree_list)), cnt, io.get_file_name(mscx_path))
    return tree_similarity

def calc_tree_similarities(mscx_path_list: list, tstree_path_list: list) -> list:
    """木の類似度を複数個計算する

    Args:
        mscx_path_list (list): MusicXMLのパスのリスト
        tstree_path_list (list): タイムスパン木のパスのリスト

    Returns:
        list: 類似度のリスト
    """

    if len(mscx_path_list) != len(tstree_path_list):
        return []

    res = []
    parser = grammar_parser.GrammarParser("ja_ginza")

    for i in range(len(mscx_path_list)):
        similarity = calc_tree_similarity(mscx_path_list[i], tstree_path_list[i], parser)
        res.append(similarity)
    
    return res