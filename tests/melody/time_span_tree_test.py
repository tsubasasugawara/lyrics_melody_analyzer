from alm.melody import time_span_tree as TST

def time_span_tree_test(in_path: str):
    ts_tree = TST.tstree_xml_2_struct(in_path)
    print(ts_tree.to_dict())

# time_span_tree_test("tests/files/オレンジ/オレンジ_A1_TS.xml", "tests/files/オレンジ/オレンジ_A1_TS.json")
time_span_tree_test("xmls/unpop_tstree/人_A1_TS.xml")
