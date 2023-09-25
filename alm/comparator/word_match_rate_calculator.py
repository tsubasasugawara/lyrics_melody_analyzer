from alm.utils import string
from alm.node import node

class WordMatchRate:
    def __init__(self, total_words_number: int, matched_words_number: int) -> None:
        """単語の一致率の計算結果を含むデータ構造

        Args:
            total_words_number (int): 単語総数
            matched_words_number (int): 一致した単語の数

        Attribute:
            section_name (str): セクション名
            total_words_number (int): 単語総数
            matched_words_number (int): 一致した単語の数
        """

        self.section_name = ""
        self.total_words_number = total_words_number
        self.matched_words_number = matched_words_number
        

def calc_word_matched_rate(words_list: list, melody_tree: node.Node) -> WordMatchRate:
    """単語の一致率を計算する

    Args:
        words_list (list): 歌詞の単語リスト
        melody_tree (node.Node): メロディの木,タイムスパン木

    Returns:
        WordMatchRate: 単語の一致率の計算結果を含むデータ構造
    """

    matched_words_count = 0
    for word_number in words_list:
        word = words_list[word_number]["word"]
        notes = words_list[word_number]["notes"]

        is_note_found = {}
        for note in notes:
            is_note_found[note] = False

        words_list[word_number]["is_matched"] = False

        melody_subtree = search_subtree(notes, melody_tree)
        # TODO: 音符がタイムスパン木に含まれていないことがある(オレンジ_A1: ひとつふた...　つ None)
        if melody_subtree == None:
            continue

        are_word_melody_matched(notes, melody_subtree, is_note_found)

        is_matched = True
        for note_id in is_note_found:
            is_matched = is_matched and is_note_found[note_id]

        if is_matched:
            matched_words_count += 1
        
        words_list[word_number]["is_matched"] = is_matched

    return WordMatchRate(len(words_list), matched_words_count)

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
