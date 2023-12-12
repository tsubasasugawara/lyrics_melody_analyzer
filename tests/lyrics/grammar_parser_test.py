from alm.lyrics import grammar_parser as gp
from alm.lyrics import lyrics_extractor as le
import pprint

def test_gramar_parser(mscx_path: str):
    parser = gp.GrammarParser("ja_ginza")
    words_dict = le.extract_lyrics(mscx_path)
    doc = parser.parse(words_dict[le.LYRICS_KEY])
    tree = parser.to_tree(doc)

    pprint.pprint(tree.to_dict())

test_gramar_parser("xmls/mscx/GReeeeN/オレンジ_S.xml")

def add_punctuation_test(lyrics: str):
    parser = gp.GrammarParser("ja_ginza")
    res = parser.add_punctuation(lyrics)
    print(res)