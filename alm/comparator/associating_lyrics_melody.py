from alm.lyrics import lyrics_extractor as LE
from alm.node import node

def associate_word_notes(lyrics_tree: node.Node, lyrics_notes_dict: node.Node) -> node.Node:
    """単語と音符を対応付ける

    Args:
        lyrics_tree (node.Node): GrammarParserクラスで出力された歌詞の木
        lyrics_notes_dict (node.Node): LyricsExtractorクラスで出力された音符と歌詞の対応を示したリスト
    
    Returns:
        node.Node: 音符を対応付けた構文解析木
    """

    words_notes_dict = {}
    explore_words_in_tree(lyrics_tree, words_notes_dict)

    associate_word_list_notes(words_notes_dict, lyrics_notes_dict)
    associate_words_tree_notes(lyrics_tree, words_notes_dict)

    return lyrics_tree

def associate_word_list_notes(words_notes_dict: dict, lyrics_notes_dict: dict) -> list:
    """単語のリストに音符を対応付ける

    Args:
        words_notes_dict (dict): 分割された単語を格納する配列
        lyrics_notes_dict (dict): LyricsExtractorクラスで出力された音符と歌詞の対応を示したリスト

    Returns:
        list: 音符を対応付けた単語のリスト
    """

    key_list = sorted(words_notes_dict)
    index_words_dict_key_list = 0

    chars = ""
    notes = []
    for index_lyrics_dict in range(0, len(lyrics_notes_dict[LE.CHAR_NOTES_KEY])):
        if index_words_dict_key_list >= len(key_list):
            break

        key = key_list[index_words_dict_key_list]
        word = words_notes_dict[key]["word"]

        chars = chars + lyrics_notes_dict[LE.CHAR_NOTES_KEY][index_lyrics_dict][LE.CHAR_KEY]
        notes.extend(lyrics_notes_dict[LE.CHAR_NOTES_KEY][index_lyrics_dict][LE.NOTES_KEY])
        notes = list(dict.fromkeys(notes))

        if word == chars:
            words_notes_dict[key]["notes"] = notes
            index_words_dict_key_list += 1

            notes = []
            chars = ""
        
    return words_notes_dict

def explore_words_in_tree(tree: node.Node, words_notes_dict: dict) -> None:
    """構文解析木から単語を探索し、単語リストを作成する

    Args:
        tree (node.Node): 構文解析木の部分木
        words_notes_dict (dict): 分割された単語を格納する配列
    """

    word = tree.word
    word_id = tree.id

    words_notes_dict[word_id] = {"word": word, "notes": []}

    for child in tree.children:
        explore_words_in_tree(child, words_notes_dict)

def associate_words_tree_notes(tree: node.Node, words_notes_dict: dict) -> None:
    """単語の木に音符を対応付ける

    Args:
        tree (node.Node): 構文解析木の部分木
        words_notes_dict (dict): 単語ごとに音符と対応付けされたマップ
    """

    word_id = tree.id
    tree.notes = words_notes_dict[word_id]["notes"]

    for child in tree.children:
        associate_words_tree_notes(child, words_notes_dict)

def associate_notes_words(words_list : dict) -> dict:
    """音符に単語を対応付ける

    Args:
        words_list (dict): 単語ごとに音符と対応付けされたマップ

    Returns:
        dict: 音符ごとに単語を対応付けたマップ
    """

    notes_word_dict = {}

    for word_num in words_list:
        for note in words_list[word_num]["notes"]:
            notes_word_dict[note] = word_num

    return notes_word_dict

def associate_tstree_words(tstree: node.Node, notes_word_dict: dict) -> None:
    """タイムスパン木のIDに単語を対応付ける

    Args:
        tstree (node.Node): タイムスパン木
        notes_word_dict (dict): 音符ごとに単語を対応付けたマップ
    """

    note_id = tstree.id
    tstree.id = notes_word_dict[note_id]
    tstree.note_id = note_id

    for child in tstree.children:
        associate_tstree_words(child, notes_word_dict)