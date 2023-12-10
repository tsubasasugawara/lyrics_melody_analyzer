from alm.comparator import *
from alm.lyrics import *
from alm.melody import *
from alm.node import node
from alm.node import node

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

    count_subtree_lyrics = {}
    extracting_subtree.count_subtree(lyrics_tree, count_subtree_lyrics)
    associating_lyrics_melody.simplify_timespan_tree(tstree)
    count_subtree_tstree = {}
    extracting_subtree.count_subtree(tstree, count_subtree_tstree)

    print(count_subtree_lyrics[lyrics_tree.id])
    print(count_subtree_tstree[tstree.id])
    # pprint.pprint(lyrics_subtree_list)
    # pprint.pprint(tstree_subtree_list)

extracting_parent_child_test("xmls/mscx/BE_FREE_A.xml", "xmls/tstree/BE_FREE_A_TS.xml")

# def extract_subtrees_test():
#     root = node.Node(
#         1,
#         [
#             node.Node(
#                 2,
#                 [
#                     node.Node(
#                         4,
#                         [],
#                         True
#                     ),
#                     node.Node(
#                         5,
#                         [],
#                         True
#                     ),
#                     node.Node(
#                         6,
#                         [],
#                         True
#                     ),
#                 ],
#                 False
#             ),
#             node.Node(
#                 3,
#                 [
#                     node.Node(
#                         7,
#                         [],
#                         True
#                     )
#                 ],
#                 False
#             ),
#         ],
#         False
#     )

#     subtree_dict = {}
#     extracting_subtree.extract_subtree(root, subtree_dict)

#     subtree_list = []
#     for _, subtrees in subtree_dict.items():
#         for subtree in subtrees:
#             subtree_list.append(subtree)

#     subtree_test = [
#         node.Node(2, [node.Node(4, [], True)], False),
#         node.Node(2, [node.Node(5, [], True)], False),
#         node.Node(2, [node.Node(6, [], True)], False),
#         node.Node(2, [node.Node(4, [], True), node.Node(5, [], True)], False),
#         node.Node(2, [node.Node(5, [], True), node.Node(6, [], True)], False),
#         node.Node(2, [node.Node(4, [], True), node.Node(6, [], True)], False),
#         node.Node(2, [node.Node(4, [], True), node.Node(5, [], True), node.Node(6, [], True)], False),
#         node.Node(3, [node.Node(7, [], True)], False),
#         node.Node(1, [node.Node(2, [], True)], False),
#         node.Node(1, [node.Node(3, [], True)], False),
#         node.Node(1, [node.Node(2, [], True), node.Node(3, [], True)], False),
#         node.Node(1, [node.Node(3, [node.Node(7, [], True)], False)], False),
#         node.Node(1, [node.Node(2, [], True), node.Node(3, [node.Node(7, [], True)], False)], False),
#         node.Node(1, [node.Node(2, [node.Node(4, [], True)], False),], False),
#         node.Node(1, [node.Node(2, [node.Node(5, [], True)], False),], False),
#         node.Node(1, [node.Node(2, [node.Node(6, [], True)], False),], False),
#         node.Node(1, [node.Node(2, [node.Node(4, [], True), node.Node(5, [], True)], False),], False),
#         node.Node(1, [node.Node(2, [node.Node(5, [], True), node.Node(6, [], True)], False),], False),
#         node.Node(1, [node.Node(2, [node.Node(4, [], True), node.Node(6, [], True)], False),], False),
#         node.Node(1, [node.Node(2, [node.Node(4, [], True), node.Node(5, [], True), node.Node(6, [], True)], False),], False),
#         node.Node(1, [node.Node(2, [node.Node(4, [], True)], False), node.Node(3, [], True)], False),
#         node.Node(1, [node.Node(2, [node.Node(5, [], True)], False), node.Node(3, [], True)], False),
#         node.Node(1, [node.Node(2, [node.Node(6, [], True)], False), node.Node(3, [], True)], False),
#         node.Node(1, [node.Node(2, [node.Node(4, [], True), node.Node(5, [], True)], False), node.Node(3, [], True)], False),
#         node.Node(1, [node.Node(2, [node.Node(5, [], True), node.Node(6, [], True)], False), node.Node(3, [], True)], False),
#         node.Node(1, [node.Node(2, [node.Node(4, [], True), node.Node(6, [], True)], False), node.Node(3, [], True)], False),
#         node.Node(1, [node.Node(2, [node.Node(4, [], True), node.Node(5, [], True), node.Node(6, [], True)], False), node.Node(3, [], True)], False),
#         node.Node(1, [node.Node(2, [node.Node(4, [], True)], False), node.Node(3, [node.Node(7, [], True)], False)], False),
#         node.Node(1, [node.Node(2, [node.Node(5, [], True)], False), node.Node(3, [node.Node(7, [], True)], False)], False),
#         node.Node(1, [node.Node(2, [node.Node(6, [], True)], False), node.Node(3, [node.Node(7, [], True)], False)], False),
#         node.Node(1, [node.Node(2, [node.Node(4, [], True), node.Node(5, [], True)], False), node.Node(3, [node.Node(7, [], True)], False)], False),
#         node.Node(1, [node.Node(2, [node.Node(5, [], True), node.Node(6, [], True)], False), node.Node(3, [node.Node(7, [], True)], False)], False),
#         node.Node(1, [node.Node(2, [node.Node(4, [], True), node.Node(6, [], True)], False), node.Node(3, [node.Node(7, [], True)], False)], False),
#         node.Node(1, [node.Node(2, [node.Node(4, [], True), node.Node(5, [], True), node.Node(6, [], True)], False), node.Node(3, [node.Node(7, [], True)], False)], False),
#     ]

#     matched_cnt = 0
#     for subtree in subtree_list:
#         subtree_dict = subtree.to_dict()
#         for test_subtree in subtree_test:
#             if  subtree_dict == test_subtree.to_dict():
#                 matched_cnt += 1
    
#     print(matched_cnt / len(subtree_list), len(subtree_test))
    
# extract_subtrees_test()

def count_subtree_test():
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
                        5,
                        [],
                        True,
                        3
                    ),
                    node.Node(
                        6,
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
                        7,
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

    count_subtree_map = {}
    extracting_subtree.count_subtree(root, count_subtree_map)
    print(count_subtree_map[root.id])

count_subtree_test()