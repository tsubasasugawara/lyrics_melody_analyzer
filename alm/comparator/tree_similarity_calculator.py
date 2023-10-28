from alm.comparator import *
from alm.lyrics import *
from alm.melody import *
from alm.utils import io
from alm.node import node as nd
import os
import glob

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

    def print(self):
        print(f"{self.section_name}\n分母：{self.denominator}\n分子：{self.numerator}\n類似度:{self.numerator/self.denominator}")

    def calc_similarity(self) -> float:
        """類似度を計算する

        Returns:
            float: 類似度
        """

        return self.numerator / self.denominator

def gen_tree(mscx_path: str, tstree_path: str, parser: grammar_parser.GrammarParser) -> list:
    """係り受け木とタイムスパン木のNodeオブジェクトを生成

    Args:
        mscx_path (str): MusicXMLのパス
        tstree_path (str): タイムスパン木のパス
        parser (grammar_parser.GrammarParser): 文法の分析に使用する

    Returns:
        list: 係り受け木(0番目)とタイムスパン木(1番目)。
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

    return [lyrics_tree, tstree]


def calc_tree_similarity(mscx_path: str, tstree_path: str, parser: grammar_parser.GrammarParser) -> TreeSimilarity:
    """木の類似度を親子関係から計算する

    Args:
        mscx_path (str): MusicXMLのパス
        tstree_path (str): タイムスパン木のパス
        parser (grammar_parser.GrammarParser): 文法の分析に使用する

    Returns:
        _type_: _description_
    """

    # MusicXMLとタイムスパン木のXMLから木構造を生成
    res = gen_tree(mscx_path, tstree_path, parser)
    lyrics_tree = res[0]
    tstree = res[1]
    associating_lyrics_melody.simplify_timespan_tree(tstree)

    # 歌詞とメロディのタイムスパン木の総数を求める
    count_lyrics_subtree_map = {}
    count_ts_subtree_map = {}
    extracting_subtree.count_subtree(lyrics_tree, count_lyrics_subtree_map)
    extracting_subtree.count_subtree(tstree, count_ts_subtree_map)
    count_lyrics_subtree = count_lyrics_subtree_map[lyrics_tree.id]
    count_ts_subtree = count_ts_subtree_map[tstree.id]
    
    # 親子関係の部分木を抜き出す
    lyrics_subtree_list = extracting_subtree.extract_parent_child(lyrics_tree)
    ts_subtree_list = extracting_subtree.extract_parent_child(tstree)

    # 一致している親子関係の部分木を探す
    matched_parent_child_subtrees = []
    for lyrics_subtree in lyrics_subtree_list:
        for ts_subtree in ts_subtree_list:
            if lyrics_subtree.id == ts_subtree.id and   lyrics_subtree.child_id == ts_subtree.child_id:
                matched_parent_child_subtrees.append(lyrics_subtree)
    
    # 親子関係から木の再生成
    node_map = nd.NodeMap(matched_parent_child_subtrees)
    node_map.parent_child_to_dict()
    root_ids = node_map.find_roots()

    # 親子関係から再生成した木の部分木の総数を求める
    count_matched_subtree = 0
    for root_id in root_ids:
        tree = node_map.gen_tree(root_id, 1)
        count_parent_child_subtree_map = {}
        extracting_subtree.count_subtree(tree, count_parent_child_subtree_map)
        count_matched_subtree += count_parent_child_subtree_map[root_id]

    return TreeSimilarity(
                min(count_lyrics_subtree, count_ts_subtree),
                count_matched_subtree,
                io.get_file_name(mscx_path)
            )

def calc_tree_similarities(mscx_dir_path: str, tstree_dir_path: str):
    """木構造の類似度計算を行う

    Args:
        mscx_dir_path (str): MusicXMLのあるディレクトリのパス
        tstree_dir_path (str): タイムスパン木のあるディレクトリのパス
    """

    # MusicXMLのパスを取得する
    mscx_path_list = []
    for item in glob.glob(mscx_dir_path):
        mscx_path_list.append(os.path.abspath(item))
    mscx_path_list.sort()

    # タイムスパン木のパスを取得する
    tstree_path_list = []
    for item in glob.glob(tstree_dir_path):
        tstree_path_list.append(os.path.abspath(item))
    tstree_path_list.sort()

    # タイムスパン木とMusicXMLの長さが同じかを確認する
    if len(mscx_path_list) != len(tstree_path_list):
        return []
    parser = grammar_parser.GrammarParser("ja_ginza")

    # 類似度の計算
    tree_similarities = []
    for i in range(len(mscx_path_list)):
        similarity = calc_tree_similarity(mscx_path_list[i], tstree_path_list[i], parser)
        tree_similarities.append(similarity)   

    # 類似度計算の結果を整理
    tree_similarities_dict = {}
    for item in tree_similarities:
        song_name = item.section_name[:-2]
        section = item.section_name[-1]

        if song_name not in tree_similarities_dict:
            tree_similarities_dict[song_name] = [-1, -1, -1, -1]

        if section == "A":
            tree_similarities_dict[song_name][0] = item.denominator
            tree_similarities_dict[song_name][1] = item.numerator
        elif section == "S":
            tree_similarities_dict[song_name][2] = item.denominator
            tree_similarities_dict[song_name][3] = item.numerator

    res = [] 
    for key, value in tree_similarities_dict.items():
        value.insert(0, key)
        res.append(value)

    io.output_csv(
        f"./csv/tree_similarities_by_{calc_by}.csv",
        ["楽曲名", "部分木の総組み合わせ数_A", "一致した部分木数_A", "部分木の総組み合わせ数_S", "一致した部分木数_S"],
        res
    )
