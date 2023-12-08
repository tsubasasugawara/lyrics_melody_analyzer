from alm.comparator import tree_similarity_calculator as tsc
from alm.comparator import word_matched_rate_calculator as wmrc
from alm.lyrics import grammar_parser as gp
from alm.utils import io
import glob
import os

def dummy_func():
    return

def calculate_height_product_reciprocal(node1, node2):
    return 1 / (node1.depth * node2.depth)

def evaluate(mscx_dir: str, tstree_dir: str, eval_func, weighting_func, output: str):
    mscx_list = glob.glob(f"{io.put_slash_dir_path(mscx_dir)}*")
    tstree_list = glob.glob(f"{io.put_slash_dir_path(tstree_dir)}*")

    if len(mscx_list) != len(tstree_list):
        return None
    
    mscx_list.sort()
    tstree_list.sort()

    parser = gp.GrammarParser("ja_ginza")

    res = {}
    for i in range(len(mscx_list)):
        rate = None
        try:
            rate = eval_func(mscx_list[i], tstree_list[i], parser)
        except:
            continue

        song = rate.section_name[:-2]
        section = rate.section_name[-1]

        if song not in res:
            res[song] = [song, None, None, None, None]
        
        if section == "A":
            res[song][1] = rate.numerator
            res[song][2] = rate.denominator
        elif section == "S":
           res[song][3] = rate.numerator
           res[song][4] = rate.denominator

    dir_path = "./csv"
    os.makedirs(dir_path, exist_ok=True)

    io.output_csv(
        output,
        ["song", "numerator_A", "denominator_A", "numerator_S", "denominator_S"],
        res.values()
    )
