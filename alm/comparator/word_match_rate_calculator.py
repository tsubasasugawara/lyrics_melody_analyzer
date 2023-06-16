from ..utils import util

def calc_word_match_rate(words_list: list, melody_tree: dict) -> float:
    """単語の一致率を計算する

    Args:
        words_list (list): 歌詞の単語リスト
        melody_tree (dict): メロディの木,タイムスパン木

    Returns:
        float: 単語の一致率
    """

    not_found_subtree_words = 0
    matched_words_count = 0
    for word_number in words_list:
        word = words_list[word_number]["word"]
        notes = words_list[word_number]["notes"]

        is_note_found = {}
        for note in notes:
            is_note_found[note] = False

        melody_subtree = search_subtree(notes, melody_tree)
        # TODO: 音符がタイムスパン木に含まれていないことがある(オレンジ_A1: ひとつふた...　つ None)
        if melody_subtree == None:
            not_found_subtree_words += 1
            continue

        are_word_melody_matched(notes, melody_subtree, is_note_found)

        is_matched = True
        for note_id in is_note_found:
            is_matched = is_matched and is_note_found[note_id]

        if is_matched:
            matched_words_count += 1
        print(word, is_matched)

    return matched_words_count / (len(words_list) - not_found_subtree_words)

# TODO: 判定が異常
def are_word_melody_matched(notes: list, melody_subtree: dict, is_note_found: dict) -> bool:
    """単語とメロディが一致しているかどうかを求める

    Args:
        notes (list): 音符のリスト
        melody_subtree (dict): メロディの部分木

    Returns:
        bool: 一致しているかどうか
    """

    note_id = melody_subtree["id"]

    if util.contains(notes, note_id):
        is_note_found[note_id] = True
        for child in melody_subtree["children"]:
            are_word_melody_matched(notes, child, is_note_found)

def search_subtree(notes: list, melody_subtree: dict) -> dict:
    """リスト内の音符が含まれる部分木を探す

    Args:
        notes (list): 音符のリスト
        melody_subtree (dict): メロディの木の部分木

    Returns:
        dict: 部分木
    """

    if util.contains(notes, melody_subtree["id"]):
        return melody_subtree
    else:
        for child in melody_subtree["children"]:
            subtree = search_subtree(notes, child)

            if subtree != None:
                return subtree
