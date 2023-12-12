from alm.utils import io
from alm.utils import string
from alm.node import node
from alm.comparator import associating_lyrics_melody
from alm.lyrics import grammar_parser
from alm.comparator import rate

def calc_word_matched_rate(mscx_path: str, tstree_path: str, parser: grammar_parser.GrammarParser, weighting_func) -> rate.Rate:
    """単語の一致率を計算する

    Args:
        mscx_path (str): MusicXMLのパス
        tstree_path (str): タイムスパン木のパス
        parser (grammar_parser.GrammarParser): 文法の分析に使用する

    Returns:
        WordMatchRate: 単語の一致率の計算結果を含むデータ構造
    """

    res = associating_lyrics_melody.gen_trees_and_word_list(mscx_path, tstree_path, parser)
    melody_tree = res[0]
    words_list = res[2]

    matched_words_count = 0
    for word_number in words_list:
        word = words_list[word_number]["word"]
        notes = words_list[word_number]["notes"]

        is_note_found = {}
        for note in notes:
            is_note_found[note] = False

        words_list[word_number]["is_matched"] = False

        melody_subtree = search_subtree(notes, melody_tree)
        if melody_subtree == None:
            continue

        are_word_melody_matched(notes, melody_subtree, is_note_found)

        is_matched = True
        for note_id in is_note_found:
            is_matched = is_matched and is_note_found[note_id]

        if is_matched:
            matched_words_count += 1
        
        words_list[word_number]["is_matched"] = is_matched

    return rate.Rate(len(words_list), matched_words_count, io.get_file_name(mscx_path))

def are_word_melody_matched(notes: list, melody_subtree: node.Node, is_note_found: dict) -> bool:
    """単語とメロディが一致しているかどうかを求める

    Args:
        notes (list): 音符のリスト
        melody_subtree (node.Node): メロディの部分木

    Returns:
        bool: 一致しているかどうか
    """

    note_id = melody_subtree.id

    if string.contains(notes, note_id):
        is_note_found[note_id] = True
        for child in melody_subtree.children:
            are_word_melody_matched(notes, child, is_note_found)

def search_subtree(notes: list, melody_subtree: node.Node) -> node.Node:
    """リスト内の音符が含まれる部分木を探す

    Args:
        notes (list): 音符のリスト
        melody_subtree (node.Node): メロディの木の部分木

    Returns:
        node.Node: 部分木
    """

    if string.contains(notes, melody_subtree.id):
        return melody_subtree
    else:
        for child in melody_subtree.children:
            subtree = search_subtree(notes, child)

            if subtree != None:
                return subtree
