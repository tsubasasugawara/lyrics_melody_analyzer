from alm.comparator import *
from alm.lyrics import *
from alm.melody import *
from alm.node import node
import pprint

def extracting_parent_child_test(mscx_path: str, tstree_path: str):
    lyrics_notes_dict = lyrics_extractor.extract_lyrics(mscx_path)

    parser = grammar_parser.GrammarParser("ja_ginza")
    doc = parser.parse(lyrics_notes_dict[lyrics_extractor.LYRICS_KEY])
    lyrics_tree = parser.to_tree(doc)

    words_notes_dict = {}
    associating_lyrics_melody.explore_words_in_tree(lyrics_tree, words_notes_dict)
    words_list = associating_lyrics_melody.associate_word_list_notes(words_notes_dict, lyrics_notes_dict)

    tstree = time_span_tree.tstree_xml_2_struct(tstree_path)
    notes_word_dict = associating_lyrics_melody.associate_notes_words(words_list)
    
    associating_lyrics_melody.associate_tstree_words(tstree, notes_word_dict)
    associating_lyrics_melody.associate_words_tree_notes(lyrics_tree, words_notes_dict)

    lyrics_subtree_list = extracting_subtree.extract_parent_child(lyrics_tree)
    tstree_subtree_list = extracting_subtree.extract_parent_child(tstree)

    pprint.pprint(lyrics_subtree_list)
    pprint.pprint(tstree_subtree_list)

def extract_subtrees_test():
    root = node.Node(
        1,
        [
            node.Node(
                2,
                [
                    node.Node(
                        4,
                        [],
                        True
                    ),
                    node.Node(
                        5,
                        [],
                        True
                    ),
                ],
                False
            ),
            node.Node(
                3,
                [],
                True
            ),
        ],
        False
    )

    subtree_dict = {}
    extracting_subtree.extract_subtree(root, subtree_dict)

    cnt = 0
    for key, subtrees in subtree_dict.items():
        for subtree in subtrees:
            pprint.pprint(subtree.to_dict())
            cnt +=1
        print("\n")
    print(cnt)

# extracting_parent_child_test("xmls/mscx/BE_FREE_A.xml", "xmls/tstree/BE_FREE_A_TS.xml")
extract_subtrees_test()