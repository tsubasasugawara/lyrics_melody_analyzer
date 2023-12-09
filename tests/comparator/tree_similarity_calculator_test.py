from alm.comparator import tree_similarity_calculator as tsc
from alm.lyrics import grammar_parser as gp

def calc_tree_similarity_test(macx_path: str, tstree_path: str):
    similarity = tsc.calc_tree_similarity_by_parent_child(macx_path, tstree_path, gp.GrammarParser("ja_ginza"))
    print(similarity.denominator, similarity.numerator)

calc_tree_similarity_test("xmls/mscx/ヨルシカ/靴の花火_S.xml", "xmls/tstree/ヨルシカ/靴の花火_S_TS.xml")