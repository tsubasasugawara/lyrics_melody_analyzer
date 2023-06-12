from alm.comparator import lyrics_melody_matcher as LMM
from alm.lyrics import grammar_parser as GP
from alm.lyrics import lyrics_extractor as LE
from alm.utils import util

def match_words_notes_test(file_path: str):
    lyrics_notes_map = LE.abstract_lyrics(file_path)

    parser = GP.GrammarParser("ja_ginza")
    doc = parser.parse(lyrics_notes_map[LE.LYRICS_KEY])
    tree = parser.to_tree_map(doc)

    matcher = LMM.LyricsMelodyMatcher(tree, lyrics_notes_map)
    matcher.match_word_notes()
    key_list = sorted(matcher.words_notes_map)
    for key in key_list:
        print(matcher.words_notes_map[key])

    print(matcher.lyrics_tree)

match_words_notes_test("tests/test_file/オレンジ/オレンジ_A1.xml")
match_words_notes_test("tests/test_file/オレンジ/オレンジ_S1.xml")