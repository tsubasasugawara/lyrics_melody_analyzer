import sys
from alm.lyrics import *
from alm.melody import *
from alm.comparator import *
from alm.utils import io

POP_DIR = "xmls/pop/"
POP_TSTREE_DIR = "xmls/pop_tstree/"
UNPOP_DIR = "xmls/unpop/"
UNPOP_TSTREE_DIR = "xmls/unpop_tstree/"
GINZA = "ja_ginza"

def calc_word_match_rate(mscx_list: list, parser: grammar_parser.GrammarParser, word_match_rate_list:list = []) -> list:
    res = word_match_rate_list

    for mscx_path in sorted(mscx_list):
        ts_path = mscx_path.replace("pop", "pop_tstree")
        ts_path = ts_path.replace(".xml", "_TS.xml")

        lyrics_notes_map = lyrics_extractor.extract_lyrics(mscx_path)
        doc = parser.parse(lyrics_notes_map[lyrics_extractor.LYRICS_KEY])
        lyrics_tree = parser.to_tree(doc)
        words_notes_map = {}
        associating_lyrics_melody.explore_words_in_tree(lyrics_tree, words_notes_map)
        words_list = associating_lyrics_melody.associate_word_list_notes(words_notes_map, lyrics_notes_map)

        melody_tree = time_span_tree.time_span_tree_to_dict(ts_path)

        rate = word_match_rate_calculator.calc_word_match_rate(words_list, melody_tree)
        rate .section_name = io.get_file_name(mscx_path)

        res.append([rate.section_name, rate.words_number, rate.match_words_number, rate.words_number - rate.match_words_number, rate.match_rate])
    
    return res

def output_word_match_rate_csv() -> None:
    parser = grammar_parser.GrammarParser(GINZA)

    pop_xmls = io.get_file_list(POP_DIR, io.XML)
    res = calc_word_match_rate(pop_xmls, parser)
    
    unpop_xmls = io.get_file_list(UNPOP_DIR, io.XML)
    res = calc_word_match_rate(unpop_xmls, parser, res)

    io.output_csv("./word_match_rate.csv", ["セクション名", "単語数", "一致した単語数", "一致しなかった単語数", "一致率"], res)

    return res

def main(argv):
    if len(argv) <= 1:
        return

    if argv[1] == "word-match-rate":
        if len(argv) >= 2:
            res = calc_word_match_rate([argv[2]], grammar_parser.GrammarParser(GINZA))
            data = res[0]
            print(f"{data[0]}\n単語数：　　　　　　　{data[1]}\n一致した単語数：　　　{data[2]}\n一致しなかった単語数：{data[3]}\n一致率：　　　　　　　{data[4]}")
        else:
            res = output_word_match_rate_csv()

if __name__ == "__main__":
    sys.exit(main(sys.argv))