from alm.comparator import tree_similarity_calculator

def calc_tree_similarity_test(macx_path: str, tstree_path: str):
    similarity = tree_similarity_calculator.calc_tree_similarity(macx_path, tstree_path)
    print(similarity.denominator, similarity.numerator, similarity.calc_similarity())

calc_tree_similarity_test("xmls/pop/オレンジ_A1.xml", "xmls/pop_tstree/オレンジ_A1_TS.xml")