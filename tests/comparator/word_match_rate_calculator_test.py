from alm.lyrics import lyrics_extractor as LE
from alm.lyrics import grammar_parser as GP
from alm.comparator import associating_lyrics_melody as LMM
from alm.comparator import word_match_rate_calculator as WMRC
from alm.melody import time_span_tree as TST
from alm.utils import util

def calc_word_match_rate_test(test_cases: list):
    parser = GP.GrammarParser("ja_ginza")

    for ele in test_cases:
        lyrics_notes_map = LE.extract_lyrics(ele[0])
        doc = parser.parse(lyrics_notes_map[LE.LYRICS_KEY])
        tree = parser.to_tree_map(doc)

        words_notes_map = {}
        LMM.explore_words_in_tree(tree, words_notes_map)
        words_list = LMM.associate_word_list_notes(words_notes_map, lyrics_notes_map)

        melody_tree = TST.time_span_tree_to_dict(ele[1])

        match_rate = WMRC.calc_word_match_rate(words_list, melody_tree)

        print(match_rate)

test_cases = [
    ["tests/files/オレンジ/オレンジ_A1_1.xml", "tests/files/オレンジ/オレンジ_A1_1_TS.xml"],
    ["tests/files/オレンジ/オレンジ_A1_2.xml", "tests/files/オレンジ/オレンジ_A1_2_TS.xml"],
    ["tests/files/オレンジ/オレンジ_A2.xml", "tests/files/オレンジ/オレンジ_A2_TS.xml"],
    ["tests/files/キセキ/キセキ_A1.xml", "tests/files/キセキ/キセキ_A1_TS.xml"],
    ["tests/files/キセキ/キセキ_A2.xml", "tests/files/キセキ/キセキ_A2_TS.xml"],
    ["tests/files/キセキ/キセキ_S1.xml", "tests/files/キセキ/キセキ_S1_TS.xml"],
    ["tests/files/キセキ/キセキ_S2.xml", "tests/files/キセキ/キセキ_S2_TS.xml"],
    ["tests/files/愛唄/愛唄_A1.xml", "tests/files/愛唄/愛唄_A1_TS.xml"],
    ["tests/files/愛唄/愛唄_A2.xml", "tests/files/愛唄/愛唄_A2_TS.xml"],
    ["tests/files/愛唄/愛唄_S1.xml", "tests/files/愛唄/愛唄_S1_TS.xml"],
    ["tests/files/愛唄/愛唄_S2.xml", "tests/files/愛唄/愛唄_S2_TS.xml"],
]

calc_word_match_rate_test(test_cases)