from alm.comparator import associating_lyrics_melody as LMM
from alm.lyrics import grammar_parser as GP
from alm.lyrics import lyrics_extractor as LE
from alm.melody import time_span_tree as TST
from alm.node import node
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

def associate_words_tree_notes(mscx_path: str, ts_path: str):
    lyrics_notes_dict = LE.extract_lyrics(mscx_path)

    parser = GP.GrammarParser("ja_ginza")
    doc = parser.parse(lyrics_notes_dict[LE.LYRICS_KEY])
    tree = parser.to_tree(doc)

    words_notes_dict = {}
    LMM.explore_words_in_tree(tree, words_notes_dict)

def associate_notes_words(mscx_path: str):
    lyrics_notes_dict = LE.extract_lyrics(mscx_path)

    parser = GP.GrammarParser("ja_ginza")
    doc = parser.parse(lyrics_notes_dict[LE.LYRICS_KEY])
    tree = parser.to_tree(doc)

    words_notes_dict = {}
    LMM.explore_words_in_tree(tree, words_notes_dict)
    words_list = LMM.associate_word_list_notes(words_notes_dict, lyrics_notes_dict)
    pprint.pprint(LMM.associate_notes_words(words_list))

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

def simplify_tstree_test():
    root = node.Node(
        1,
        [
            node.Node(
                2,
                [
                    node.Node(
                        4,
                        [],
                        True,
                        3
                    ),
                    node.Node(
                        3,
                        [],
                        True,
                        3
                    ),
                    node.Node(
                        1,
                        [],
                        True,
                        3
                    ),
                ],
                False,
                2
            ),
            node.Node(
                3,
                [
                    node.Node(
                        2,
                        [],
                        True,
                        3
                    )
                ],
                False,
                2
            ),
        ],
        False,
        1
    )

    LMM.simplify_timespan_tree(root)
    pprint.pprint(root.to_dict())

simplify_tstree_test()