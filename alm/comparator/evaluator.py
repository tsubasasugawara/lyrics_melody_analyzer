from alm.comparator import tree_similarity_calculator as tsc
from alm.comparator import word_matched_rate_calculator as wmrc
from alm.lyrics import grammar_parser as gp
from alm.utils import io
import glob

def weighting_func(data):
    return data

def evaluate(mscx_dir: str, tstree_dir: str, eval_func):
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
        rate = weighting_func(rate)

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

    io.output_csv(
        f"./csv/{io.get_file_name(mscx_dir)}_{mode}_{io.get_now_date()}.csv",
        ["song", "numerator_A", "denominator_A", "numerator_S", "denominator_S"],
        res.values()
    )
