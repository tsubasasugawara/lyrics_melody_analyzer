from alm.comparator import lyrics_melody_matcher as LMM
from alm.lyrics.grammar import grammar_parser as GP
from alm.lyrics.extractor import lyrics_extractor
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

make_words_notes_map_test()