from alm.comparator import rate
from alm.comparator import associating_lyrics_melody as alm
from alm.comparator import extracting_subtree as es
from alm.lyrics import grammar_parser as gp
from alm.utils import io
from alm.node import node as nd
from alm.comparator import evaluator
import timeout_decorator

@timeout_decorator.timeout(1)
def calc_tree_similarity(mscx_path: str, tstree_path: str, parser: gp.GrammarParser) -> rate.Rate:
    """木の類似度を親子関係から計算する

    Args:
        mscx_path (str): MusicXMLのパス
        tstree_path (str): タイムスパン木のパス
        parser (grammar_parser.GrammarParser): 文法の分析に使用する

    Returns:
        _type_: _description_
    """

    # MusicXMLとタイムスパン木のXMLから木構造を生成
    res = alm.gen_trees_and_word_list(mscx_path, tstree_path, parser, alm.TREE_SIMILARITY)
    tstree = res[0]
    lyrics_tree = res[1]

    # 歌詞とメロディのタイムスパン木の総数を求める
    count_lyrics_subtree_map = {}
    count_ts_subtree_map = {}
    es.count_subtree(lyrics_tree, count_lyrics_subtree_map)
    es.count_subtree(tstree, count_ts_subtree_map)
    count_lyrics_subtree = count_lyrics_subtree_map[lyrics_tree.id]
    count_ts_subtree = count_ts_subtree_map[tstree.id]
    
    # 親子関係の部分木を抜き出す
    lyrics_subtree_list = es.extract_parent_child(lyrics_tree)
    ts_subtree_list = es.extract_parent_child(tstree)

    # 一致している親子関係の部分木を探す
    matched_parent_child_subtrees = []
    for lyrics_subtree in lyrics_subtree_list:
        for ts_subtree in ts_subtree_list:
            if lyrics_subtree.id == ts_subtree.id and lyrics_subtree.child_id == ts_subtree.child_id:
                matched_parent_child_subtrees.append(lyrics_subtree)
                break
    
    # 親子関係から木の再生成
    node_map = nd.NodeMap(matched_parent_child_subtrees)
    node_map.parent_child_to_dict()
    root_ids = node_map.find_roots()

    # 親子関係から再生成した木の部分木の総数を求める
    count_matched_subtree = 0
    for root_id in root_ids:
        tree = node_map.gen_tree(root_id, 1)
        count_parent_child_subtree_map = {}
        es.count_subtree(tree, count_parent_child_subtree_map)
        count_matched_subtree += count_parent_child_subtree_map[root_id]

    return rate.Rate(
                min(count_lyrics_subtree, count_ts_subtree),
                count_matched_subtree,
                io.get_file_name(mscx_path)
            )

def __get_max_depth(tree:nd.Node):
    depth = tree.depth
    for child in tree.children:
        depth = max(depth, __get_max_depth(child))
    return depth

def calc_tree_similarity_by_parent_child(mscx_path: str, tstree_path: str, parser: gp.GrammarParser, weighting_func=evaluator.weight0) -> rate.Rate:
    # MusicXMLとタイムスパン木のXMLから木構造を生成
    res = alm.gen_trees_and_word_list(mscx_path, tstree_path, parser, alm.TREE_SIMILARITY)
    tstree = res[0]
    lyrics_tree = res[1]

    ts_max_depth = __get_max_depth(tstree)
    lt_max_depth = __get_max_depth(lyrics_tree)

    # 親子関係の部分木を抜き出す
    lyrics_subtree_list = es.extract_parent_child(lyrics_tree)
    ts_subtree_list = es.extract_parent_child(tstree)

    res = rate.Rate(
                denominator=0,
                numerator=0,
                section_name=io.get_file_name(mscx_path)
            )
    
    for lyrics_subtree in lyrics_subtree_list:
        depth_l = lt_max_depth - lyrics_subtree.depth + 1
        weight = weighting_func(depth_l, ts_max_depth - ts_subtree_list[0].depth + 1)
        is_matched = False
        for ts_subtree in ts_subtree_list:
            depth_t = ts_max_depth - ts_subtree.depth + 1
            # 同じ親子の部分木が存在することがあるが、それは複数の単語が一つの音符に対応しているのを分割したため
            if lyrics_subtree.id == ts_subtree.id and lyrics_subtree.child_id == ts_subtree.child_id:
                is_matched = True
                res.numerator += weighting_func(depth_l, depth_t)
                res.denominator += weighting_func(depth_l, depth_t)
                weight = min(weight, weighting_func(depth_l, depth_t))
        if not is_matched:
            res.denominator += weight
    
    return res
