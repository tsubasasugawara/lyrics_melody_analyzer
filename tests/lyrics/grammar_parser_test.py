from alm.lyrics import grammar_parser as gp
from alm.utils import util

def test_gramar_parser():
    parser = gp.GrammarParser("ja_ginza")
    parser.parse("明日、今日よりも好きになれる。あふれる思いが止まらない。")
    parser.to_tree_map()

    print(parser.tree)

    util.output_json("tests/test_file/grammar_parser_test.json", parser.tree)

test_gramar_parser()