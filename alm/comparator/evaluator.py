from alm.comparator import tree_similarity_calculator as tsc
from alm.comparator import word_matched_rate_calculator as wmrc
from alm.lyrics import grammar_parser as gp
from alm.utils import io
import glob

WORD_MATCHED_RATE = "word_matched_rate"
SUBTREE_COUNT = "tree_similarity_by_subtree_count"
PARENT_CHILD = "tree_similarity_by_parent_child"

def evaluate(mscx_dir: str, tstree_dir: str, mode: str):
    mscx_list = glob.glob(f"{io.put_slash_dir_path(mscx_dir)}*")
    tstree_list = glob.glob(f"{io.put_slash_dir_path(tstree_dir)}*")

    if len(mscx_list) != len(tstree_list):
        return None
    
    mscx_list.sort()
    tstree_list.sort()

    parser = gp.GrammarParser("ja_ginza")

    # ts_modeをもとに評価関数を決定する
    eval_func = None
    if mode == WORD_MATCHED_RATE:
        eval_func = wmrc.calc_word_matched_rate
    elif mode == SUBTREE_COUNT:
        eval_func = tsc.calc_tree_similarity
    elif mode == PARENT_CHILD:
        eval_func = tsc.calc_tree_similarity_by_parent_child
    else:
        return

    res = {}
    for i in range(len(mscx_list)):
        #TODO: tree_similarityをrateにへんこう
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
            res[song][1] = tree_similarity.numerator
            res[song][2] = tree_similarity.denominator
        elif section == "S":
           res[song][3] = tree_similarity.numerator
           res[song][4] = tree_similarity.denominator

    io.output_csv(
        f"./csv/{io.get_file_name(mscx_dir)}_{mode}_{io.get_now_date()}.csv",
        ["song", "numerator_A", "denominator_A", "numerator_S", "denominator_S"],
        res.values()
    )
