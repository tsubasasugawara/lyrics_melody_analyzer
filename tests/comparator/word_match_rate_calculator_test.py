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

        res = WMRC.calc_word_match_rate(words_list, melody_tree)
        res.section_name = ele[2]

        print(res.section_name, res.words_number, res.match_words_number, res.match_rate)
        words = [" " for i in range(len(words_list))]
        for i in words_list:
            words[i] = words_list[i]["word"] + str(words_list[i]["is_matched"])
        print(words, "\n")

def word_match_rate_to_csv(test_cases: list, csv_path: str):
    parser = GP.GrammarParser("ja_ginza")

    csv_data = []

    for ele in test_cases:
        lyrics_notes_map = LE.extract_lyrics(ele[0])
        doc = parser.parse(lyrics_notes_map[LE.LYRICS_KEY])
        tree = parser.to_tree_map(doc)

        words_notes_map = {}
        LMM.explore_words_in_tree(tree, words_notes_map)
        words_list = LMM.associate_word_list_notes(words_notes_map, lyrics_notes_map)

        melody_tree = TST.time_span_tree_to_dict(ele[1])

        res = WMRC.calc_word_match_rate(words_list, melody_tree)
        res.section_name = ele[2]

        csv_data.append([res.section_name, res.words_number, res.match_words_number, res.words_number - res.match_words_number, res.match_rate])
    
    util.output_csv(csv_path, ["セクション名", "単語数", "一致した単語数", "一致しなかった単語数", "一致率"], csv_data)

test_cases = [
#    ["tests/files/オレンジ/オレンジ_A1_1.xml", "tests/files/オレンジ/オレンジ_A1_1_TS.xml"],
#    ["tests/files/オレンジ/オレンジ_A1_2.xml", "tests/files/オレンジ/オレンジ_A1_2_TS.xml"],
#    ["tests/files/オレンジ/オレンジ_A2.xml", "tests/files/オレンジ/オレンジ_A2_TS.xml"],
#    ["tests/files/キセキ/キセキ_A1.xml", "tests/files/キセキ/キセキ_A1_TS.xml"],
#    ["tests/files/キセキ/キセキ_A2.xml", "tests/files/キセキ/キセキ_A2_TS.xml"],
#    ["tests/files/キセキ/キセキ_S1.xml", "tests/files/キセキ/キセキ_S1_TS.xml"],
#    ["tests/files/キセキ/キセキ_S2.xml", "tests/files/キセキ/キセキ_S2_TS.xml"],
#    ["tests/files/愛唄/愛唄_A1.xml", "tests/files/愛唄/愛唄_A1_TS.xml"],
#    ["tests/files/愛唄/愛唄_A2.xml", "tests/files/愛唄/愛唄_A2_TS.xml"],
#    ["tests/files/愛唄/愛唄_S1.xml", "tests/files/愛唄/愛唄_S1_TS.xml"],
#    ["tests/files/愛唄/愛唄_S2.xml", "tests/files/愛唄/愛唄_S2_TS.xml"],
    ["tests/files/popular/キセキ_A1.xml", "tests/files/popular/キセキ_A1_TS.xml", "キセキ_A1"],
    ["tests/files/popular/キセキ_A2.xml", "tests/files/popular/キセキ_A2_TS.xml", "キセキ_A2"],
    ["tests/files/popular/キセキ_S1.xml", "tests/files/popular/キセキ_S1_TS.xml", "キセキ_S1"],
    ["tests/files/popular/キセキ_S2.xml", "tests/files/popular/キセキ_S2_TS.xml", "キセキ_S2"],
    ["tests/files/popular/キセキ_S3.xml", "tests/files/popular/キセキ_S3_TS.xml", "キセキ_S3"],
    ["tests/files/popular/愛唄_A1.xml", "tests/files/popular/愛唄_A1_TS.xml", "愛唄_A1"],
    ["tests/files/popular/愛唄_A2.xml", "tests/files/popular/愛唄_A2_TS.xml", "愛唄_A2"],
    ["tests/files/popular/愛唄_S1.xml", "tests/files/popular/愛唄_S1_TS.xml", "愛唄_S1"],
    ["tests/files/popular/愛唄_S2.xml", "tests/files/popular/愛唄_S2_TS.xml", "愛唄_S2"],
    ["tests/files/popular/花唄_A1.xml", "tests/files/popular/花唄_A1_TS.xml", "花唄_A1"],
    ["tests/files/popular/花唄_A2.xml", "tests/files/popular/花唄_A2_TS.xml", "花唄_A2"],
    ["tests/files/popular/花唄_S1.xml", "tests/files/popular/花唄_S1_TS.xml", "花唄_S1"],
    ["tests/files/popular/花唄_S2.xml", "tests/files/popular/花唄_S2_TS.xml", "花唄_S2"],
    ["tests/files/popular/オレンジ_A1.xml", "tests/files/popular/オレンジ_A1_TS.xml", "オレンジ_A1"],
    ["tests/files/popular/オレンジ_A2.xml", "tests/files/popular/オレンジ_A2_TS.xml", "オレンジ_A2"],
    ["tests/files/popular/オレンジ_S1.xml", "tests/files/popular/オレンジ_S1_TS.xml", "オレンジ_S1"],
    ["tests/files/popular/オレンジ_S2.xml", "tests/files/popular/オレンジ_S2_TS.xml", "オレンジ_S2"],
    ["tests/files/popular/オレンジ_S3.xml", "tests/files/popular/オレンジ_S3_TS.xml", "オレンジ_S3"],
    ["tests/files/popular/オレンジ_S4.xml", "tests/files/popular/オレンジ_S4_TS.xml", "オレンジ_S4"],
    ["tests/files/popular/遥か_A1.xml", "tests/files/popular/遥か_A1_TS.xml", "遥か_A1"],
    ["tests/files/popular/遥か_A2.xml", "tests/files/popular/遥か_A2_TS.xml", "遥か_A2"],
    ["tests/files/popular/遥か_A3.xml", "tests/files/popular/遥か_A3_TS.xml", "遥か_A3"],
    ["tests/files/popular/遥か_A4.xml", "tests/files/popular/遥か_A4_TS.xml", "遥か_A4"],
    ["tests/files/popular/遥か_S1.xml", "tests/files/popular/遥か_S1_TS.xml", "遥か_S1"],
    ["tests/files/popular/遥か_S2.xml", "tests/files/popular/遥か_S2_TS.xml", "遥か_S2"],
    ["tests/files/unpopular/beautiful_days_A1.xml", "tests/files/unpopular/beautiful_days_A1_TS.xml", "beautiful_days_A1"],
    ["tests/files/unpopular/beautiful_days_A2.xml", "tests/files/unpopular/beautiful_days_A2_TS.xml", "beautiful_days_A2"],
    ["tests/files/unpopular/beautiful_days_S1.xml", "tests/files/unpopular/beautiful_days_S1_TS.xml", "beautiful_days_S1"],
    ["tests/files/unpopular/beautiful_days_S2.xml", "tests/files/unpopular/beautiful_days_S2_TS.xml", "beautiful_days_S2"],
    ["tests/files/unpopular/ビリーヴ_A1.xml", "tests/files/unpopular/ビリーヴ_A1_TS.xml", "ビリーヴ_A1"],
    ["tests/files/unpopular/ビリーヴ_A2.xml", "tests/files/unpopular/ビリーヴ_A2_TS.xml", "ビリーヴ_A2"],
    ["tests/files/unpopular/ビリーヴ_S1.xml", "tests/files/unpopular/ビリーヴ_S1_TS.xml", "ビリーヴ_S1"],
    ["tests/files/unpopular/ビリーヴ_S2.xml", "tests/files/unpopular/ビリーヴ_S2_TS.xml", "ビリーヴ_S2"],
    ["tests/files/unpopular/たけてん_A1.xml", "tests/files/unpopular/たけてん_A1_TS.xml", "たけてん_A1"],
    ["tests/files/unpopular/たけてん_A2.xml", "tests/files/unpopular/たけてん_A2_TS.xml", "たけてん_A2"],
    ["tests/files/unpopular/たけてん_S1.xml", "tests/files/unpopular/たけてん_S1_TS.xml", "たけてん_S1"],
    ["tests/files/unpopular/たけてん_S2.xml", "tests/files/unpopular/たけてん_S2_TS.xml", "たけてん_S2"],
    ["tests/files/unpopular/人_A1.xml", "tests/files/unpopular/人_A1_TS.xml", "人_A1"],
    ["tests/files/unpopular/人_A2.xml", "tests/files/unpopular/人_A2_TS.xml", "人_A2"],
    ["tests/files/unpopular/人_S1.xml", "tests/files/unpopular/人_S1_TS.xml", "人_S1"],
    ["tests/files/unpopular/人_S2.xml", "tests/files/unpopular/人_S2_TS.xml", "人_S2"],
    ["tests/files/unpopular/蕾_S1.xml", "tests/files/unpopular/蕾_S1_TS.xml", "蕾_S1"],
    ["tests/files/unpopular/蕾_S2.xml", "tests/files/unpopular/蕾_S2_TS.xml", "蕾_S2"],
    ["tests/files/unpopular/蕾_S3.xml", "tests/files/unpopular/蕾_S3_TS.xml", "蕾_S3"],
]

calc_word_match_rate_test(test_cases)
word_match_rate_to_csv(test_cases, "tests/files/word_match_rate_result.csv")