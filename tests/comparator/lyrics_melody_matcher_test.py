from alm.comparator import lyrics_melody_matcher as LMM
from alm.lyrics import grammar_parser as GP
from alm.lyrics import lyrics_extractor
from alm.utils import util

def make_words_notes_map_test():
    e = lyrics_extractor.LyricsExtractor()
    e.abstract_lyrics("tests/test_file/オレンジ_A1/オレンジ_A1.xml")

    parser = GP.GrammarParser("ja_ginza")
    parser.parse(e.lyrics)
    parser.to_tree_map()

    matcher = LMM.LyricsMelodyMatcher(parser.tree, e.lyrics_notes_map)
    key_list = sorted(matcher.words_notes_map)
    for key in key_list:
        print(matcher.words_notes_map[key])

def match_words_notes_test(file_path: str):
    e = lyrics_extractor.LyricsExtractor()
    e.abstract_lyrics(file_path)

    parser = GP.GrammarParser("ja_ginza")
    parser.parse(e.lyrics)
    parser.to_tree_map()

    matcher = LMM.LyricsMelodyMatcher(parser.tree, e.lyrics_notes_map)
    matcher.match_word_notes()
    key_list = sorted(matcher.words_notes_map)
    for key in key_list:
        print(matcher.words_notes_map[key])

    print(matcher.lyrics_tree)

    util.output_json("tests/test_file/mapping_word_notes_test.json", matcher.lyrics_tree)

match_words_notes_test("tests/test_file/オレンジ/オレンジ_A1.xml")
match_words_notes_test("tests/test_file/オレンジ/オレンジ_S1.xml")