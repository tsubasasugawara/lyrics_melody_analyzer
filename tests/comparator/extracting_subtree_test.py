from alm.comparator import *
from alm.lyrics import *
from alm.melody import *
import pprint

def extracting_parent_child_test(mscx_path: str, tstree_path: str):
    lyrics_notes_map = lyrics_extractor.extract_lyrics(mscx_path)

    parser = grammar_parser.GrammarParser("ja_ginza")
    doc = parser.parse(lyrics_notes_map[lyrics_extractor.LYRICS_KEY])
    lyrics_tree = parser.to_tree(doc)

    words_notes_map = {}
    associating_lyrics_melody.explore_words_in_tree(lyrics_tree, words_notes_map)
    words_list = associating_lyrics_melody.associate_word_list_notes(words_notes_map, lyrics_notes_map)

    tstree = time_span_tree.tstree_xml_2_struct(tstree_path)
    notes_word_map = associating_lyrics_melody.associate_notes_words(words_list)
    
    associating_lyrics_melody.associate_tstree_words(tstree, notes_word_map)
    associating_lyrics_melody.associate_words_tree_notes(lyrics_tree, words_notes_map)

    lyrics_subtree_list = extracting_subtree.extract_parent_child(lyrics_tree)
    tstree_subtree_list = extracting_subtree.extract_parent_child(tstree)

    pprint.pprint(lyrics_subtree_list)
    pprint.pprint(tstree_subtree_list)

extracting_parent_child_test("xmls/pop/BE_FREE_A.xml", "xmls/pop_tstree/BE_FREE_A_TS.xml")
