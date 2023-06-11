from alm.melody import time_span_tree as TST

def time_span_tree_test(in_path: str, out_path: str):
    tstree = TST.TimeSpanTree()
    tstree.time_span_tree_to_dict(in_path)
    tstree.to_json(out_path)
    print(tstree.time_span_tree_dict)

time_span_tree_test("tests/test_file/オレンジ/オレンジ_A1_TS.xml", "tests/test_file/オレンジ/オレンジ_A1_TS.json")
