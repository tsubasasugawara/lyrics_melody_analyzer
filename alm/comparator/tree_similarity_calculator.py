from alm.comparator import rate
from alm.comparator import associating_lyrics_melody as alm
from alm.comparator import extracting_subtree as es
from alm.lyrics import grammar_parser as gp
from alm.utils import io
from alm.node import node as nd
import glob
import timeout_decorator

SUBTREE_COUNT = "subtree_count"
PARENT_CHILD = "parent_child"

@timeout_decorator.timeout(10)
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

def calc_tree_similarity_by_parent_child(mscx_path: str, tstree_path: str, parser: gp.GrammarParser) -> rate.Rate:
    # MusicXMLとタイムスパン木のXMLから木構造を生成
    res = alm.gen_trees_and_word_list(mscx_path, tstree_path, parser, alm.TREE_SIMILARITY)
    tstree = res[0]
    lyrics_tree = res[1]

    # 親子関係の部分木を抜き出す
    lyrics_subtree_list = es.extract_parent_child(lyrics_tree)
    ts_subtree_list = es.extract_parent_child(tstree)

    res = rate.Rate(
                denominator=min(len(lyrics_subtree_list), len(ts_subtree_list)),
                numerator=0,
                section_name=io.get_file_name(mscx_path)
            )
    
    for lyrics_subtree in lyrics_subtree_list:
        for ts_subtree in ts_subtree_list:
            if lyrics_subtree.id == ts_subtree.id and lyrics_subtree.child_id == ts_subtree.child_id:
                res.numerator += 1
                break
    
    return res

def calc_tree_similarities(mscx_dir: str, tstree_dir: str, ts_mode: str):
    mscx_list = glob.glob(f"{io.put_slash_dir_path(mscx_dir)}*")
    tstree_list = glob.glob(f"{io.put_slash_dir_path(tstree_dir)}*")

    if len(mscx_list) != len(tstree_list):
        return None
    
    mscx_list.sort()
    tstree_list.sort()

    parser = gp.GrammarParser("ja_ginza")

    # ts_modeをもとに評価関数を決定する
    eval_func = None
    if ts_mode == SUBTREE_COUNT:
        eval_func = calc_tree_similarity
    elif ts_mode == PARENT_CHILD:
        eval_func = calc_tree_similarity_by_parent_child
    else:
        return

    res = {}
    for i in range(len(mscx_list)):
        tree_similarity = None
        try:
            tree_similarity = eval_func(mscx_list[i], tstree_list[i], parser)
        except:
            continue

        song = tree_similarity.section_name[:-2]
        section = tree_similarity.section_name[-1]

        if song not in res:
            res[song] = [song, None, None, None, None]
        
        if section == "A":
            res[song][1] = tree_similarity.denominator
            res[song][2] = tree_similarity.numerator
        elif section == "S":
           res[song][3] = tree_similarity.denominator
           res[song][4] = tree_similarity.numerator

    io.output_csv(
        f"./csv/{io.get_file_name(mscx_dir)}_ts_{ts_mode}_{io.get_now_date()}.csv",
        ["song", "numerator_A", "denominator_A", "numerator_S", "denominator_S"],
        res.values()
    )
