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

        melody_subtree = search_subtree(notes, melody_tree)
        # TODO: 音符がタイムスパン木に含まれていないことがある(オレンジ_A1: ひとつふた...　つ None)
        if melody_subtree == None:
            not_found_subtree_words += 1
            continue

        is_matched = are_word_melody_matched(notes, melody_subtree)
        if is_matched:
            matched_words_count += 1

    return matched_words_count / (len(words_list) - not_found_subtree_words)

def are_word_melody_matched(notes: list, melody_subtree: dict) -> bool:
    """単語とメロディが一致しているかどうかを求める

    Args:
        notes (list): 音符のリスト
        melody_subtree (dict): メロディの部分木

    Returns:
        bool: 一致しているかどうか
    """
    if util.contains(notes, melody_subtree["id"]):
        is_matched = True
        for child in melody_subtree["children"]:
            is_matched = is_matched and are_word_melody_matched(notes, child)
        return is_matched
    else:
        return False

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
