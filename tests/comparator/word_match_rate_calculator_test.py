from alm.lyrics import lyrics_extractor as LE
from alm.lyrics import grammar_parser as GP
from alm.comparator import associating_lyrics_melody as LMM
from alm.comparator import word_match_rate_calculator as WMRC
from alm.melody import time_span_tree as TST

def calc_word_match_rate_test(xml_path: str, time_span_path: str):
    lyrics_notes_map = LE.extract_lyrics(xml_path)

    parser = GP.GrammarParser("ja_ginza")
    doc = parser.parse(lyrics_notes_map[LE.LYRICS_KEY])
    tree = parser.to_tree_map(doc)

    words_notes_map = {}
    LMM.explore_words_in_tree(tree, words_notes_map)
    words_list = LMM.associate_word_list_notes(words_notes_map, lyrics_notes_map)
    print(words_list)

    melody_tree = TST.time_span_tree_to_dict(time_span_path)

    match_rate = WMRC.calc_word_match_rate(words_list, melody_tree)

    print(match_rate)

calc_word_match_rate_test("tests/test_file/キセキ/キセキ_A1_test.xml", "tests/test_file/キセキ/キセキ_A1_TS_test.xml")
# calc_word_match_rate_test("tests/test_file/オレンジ/オレンジ_A1.xml", "tests/test_file/オレンジ/オレンジ_A1_TS.xml")