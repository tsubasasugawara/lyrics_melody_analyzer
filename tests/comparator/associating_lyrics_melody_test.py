from alm.comparator import associating_lyrics_melody as LMM
from alm.lyrics import grammar_parser as GP
from alm.lyrics import lyrics_extractor as LE
from alm.melody import time_span_tree as TST
from collections import deque
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

def __count_nodes(tree):
    cnt = 0
    id_dict = {}
    queue = deque([tree])
    while queue:
        node = queue.popleft()
        if node.id in id_dict:
            id_dict[node.id] += 1
        else:
            id_dict[node.id] = 0
        cnt += 1

        for child in node.children:
            queue.append(child)
    
    return cnt

def simplify_tstree_test():
    mscx_path = "xmls/mscx/GReeeeN/遥か_A.xml"
    ts_path = "xmls/tstree/GReeeeN/遥か_A_TS.xml"

    lyrics_notes_dict = LE.extract_lyrics(mscx_path)

    parser = GP.GrammarParser("ja_ginza")
    doc = parser.parse(lyrics_notes_dict[LE.LYRICS_KEY])
    lyrics_tree = parser.to_tree(doc)

    words_notes_dict = {}
    LMM.explore_words_in_tree(lyrics_tree, words_notes_dict)
    words_list = LMM.associate_word_list_notes(words_notes_dict, lyrics_notes_dict)
    pprint.pprint(words_list)

    tstree = TST.tstree_xml_2_struct(ts_path)

    notes_word_dict = LMM.associate_notes_words(words_list)
    LMM.associate_tstree_words(tstree, notes_word_dict)
    LMM.associate_words_tree_notes(lyrics_tree, words_notes_dict)
    LMM.copy_note_supported_multiple_word(tstree, True)
    LMM.simplify_timespan_tree(tstree)
    
    pprint.pprint(tstree.to_dict())
    print(__count_nodes(tstree), __count_nodes(lyrics_tree))

simplify_tstree_test()