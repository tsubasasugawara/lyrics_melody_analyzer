from alm.lyrics import grammar_parser as gp
from alm.utils import util

def test_gramar_parser(lyrics: str):
    parser = gp.GrammarParser("ja_ginza")
    doc = parser.parse(lyrics)
    tree = parser.to_tree(doc)

    print(tree)

test_gramar_parser("明日、今日よりも好きになれる。あふれる思いが止まらない。")

def add_punctuation_test(lyrics: str):
    parser = gp.GrammarParser("ja_ginza")
    res = parser.add_punctuation(lyrics)
    print(res)

add_punctuation_test("明日、今日よりも好きになれる。あふれる思いが止まらない。")