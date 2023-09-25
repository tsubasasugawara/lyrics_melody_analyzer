from alm.comparator import associating_lyrics_melody as LMM
from alm.lyrics import grammar_parser as GP
from alm.lyrics import lyrics_extractor as LE
from alm.melody import time_span_tree as TST
import pprint

def associate_words_notes_test(file_path: str):
    lyrics_notes_dict = LE.extract_lyrics(file_path)

    parser = GP.GrammarParser("ja_ginza")
    doc = parser.parse(lyrics_notes_dict[LE.LYRICS_KEY])
    tree = parser.to_tree(doc)

    lyrics_tree = LMM.associate_word_notes(tree, lyrics_notes_dict)
    print(lyrics_tree)

    words_notes_dict = {}
    LMM.explore_words_in_tree(tree, words_notes_dict)
    words_list = LMM.associate_word_list_notes(words_notes_dict, lyrics_notes_dict)
    print(words_list)

    print()

#associate_words_notes_test("xmls/pop/オレンジ_A1.xml")

def associate_words_tree_notes(mscx_path: str, ts_path: str):
    lyrics_notes_dict = LE.extract_lyrics(mscx_path)

    parser = GP.GrammarParser("ja_ginza")
    doc = parser.parse(lyrics_notes_dict[LE.LYRICS_KEY])
    tree = parser.to_tree(doc)

    words_notes_dict = {}
    LMM.explore_words_in_tree(tree, words_notes_dict)

associate_words_tree_notes("xmls/pop/オレンジ_A1.xml", "xmls/pop_tstree/オレンジ_A1_TS.xml")

def associate_notes_words(mscx_path: str):
    lyrics_notes_dict = LE.extract_lyrics(mscx_path)

    parser = GP.GrammarParser("ja_ginza")
    doc = parser.parse(lyrics_notes_dict[LE.LYRICS_KEY])
    tree = parser.to_tree(doc)

    words_notes_dict = {}
    LMM.explore_words_in_tree(tree, words_notes_dict)
    words_list = LMM.associate_word_list_notes(words_notes_dict, lyrics_notes_dict)
    pprint.pprint(LMM.associate_notes_words(words_list))

# associate_notes_words("xmls/pop/オレンジ_A1.xml")

def associate_tstree_words(mscx_path: str, tstree_path: str):
    lyrics_notes_dict = LE.extract_lyrics(mscx_path)

    parser = GP.GrammarParser("ja_ginza")
    doc = parser.parse(lyrics_notes_dict[LE.LYRICS_KEY])
    tree = parser.to_tree(doc)

    words_notes_dict = {}
    LMM.explore_words_in_tree(tree, words_notes_dict)
    words_list = LMM.associate_word_list_notes(words_notes_dict, lyrics_notes_dict)

    tstree = TST.tstree_xml_2_struct(tstree_path)
    notes_word_dict = LMM.associate_notes_words(words_list)
    
    LMM.associate_tstree_words(tstree, notes_word_dict)
    LMM.associate_words_tree_notes(tree, words_notes_dict)

    pprint.pprint(tstree.to_dict())
    pprint.pprint(tree.to_dict())

associate_tstree_words("xmls/pop/オレンジ_A1.xml", "xmls/pop_tstree/オレンジ_A1_TS.xml")