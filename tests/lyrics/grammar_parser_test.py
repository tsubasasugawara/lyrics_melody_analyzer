from alm.lyrics import grammar_parser as gp
from alm.utils import util

def test_gramar_parser():
    parser = gp.GrammarParser("ja_ginza")
    doc = parser.parse("明日、今日よりも好きになれる。あふれる思いが止まらない。")
    tree = parser.to_tree_map(doc)

    print(tree)

    util.output_json("tests/test_file/grammar_parser_test.json", tree)

test_gramar_parser()