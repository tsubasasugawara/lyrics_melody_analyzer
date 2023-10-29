from alm.lyrics import lyrics_extractor as LE
from alm.node import node as nd
from collections import deque
from alm.lyrics import *
from alm.melody import *

def associate_word_notes(lyrics_tree: nd.Node, lyrics_notes_dict: nd.Node) -> nd.Node:
    """単語と音符を対応付ける

    Args:
        lyrics_tree (nd.Node): GrammarParserクラスで出力された歌詞の木
        lyrics_notes_dict (nd.Node): LyricsExtractorクラスで出力された音符と歌詞の対応を示したリスト
    
    Returns:
        nd.Node: 音符を対応付けた構文解析木
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

def explore_words_in_tree(tree: nd.Node, words_notes_dict: dict) -> None:
    """構文解析木から単語を探索し、単語リストを作成する

    Args:
        tree (nd.Node): 構文解析木の部分木
        words_notes_dict (dict): 分割された単語を格納する配列
    """

    word = tree.word
    word_id = tree.id

    words_notes_dict[word_id] = {"word": word, "notes": []}

    for child in tree.children:
        explore_words_in_tree(child, words_notes_dict)

def associate_words_tree_notes(tree: nd.Node, words_notes_dict: dict) -> None:
    """単語の木に音符を対応付ける

    Args:
        tree (nd.Node): 構文解析木の部分木
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

def associate_tstree_words(tstree: nd.Node, notes_word_dict: dict) -> None:
    """タイムスパン木のIDに単語を対応付ける

    Args:
        tstree (nd.Node): タイムスパン木
        notes_word_dict (dict): 音符ごとに単語を対応付けたマップ
    """

    note_id = tstree.id
    tstree.id = notes_word_dict[note_id]
    tstree.note_id = note_id

    for child in tstree.children:
        associate_tstree_words(child, notes_word_dict)

def simplify_timespan_tree(tstree: nd.Node):
    """タイムスパン木の簡約

    Args:
        tstree (nd.Node) : 簡約化したいタイムスパン木
    """

    id_depth_map = {}
    id_depth_map[tstree.id] = tstree.depth
    queue = deque([tstree])
    while queue:
        node = queue.popleft()
        children = []

        for child in node.children:
            if child.id not in id_depth_map:
                id_depth_map[child.id] = child.depth
                children.append(child)
            else:
                children.extend(child.children)

        node.children = children
        for child in node.children:
            queue.append(child)

WORD_MATCHED_RATE = 0
TREE_SIMILARITY = 1

def gen_trees_and_word_list(mscx_path: str, tstree_path: str, parser: grammar_parser.GrammarParser, mode: int = WORD_MATCHED_RATE):
    """タイムスパン木、係り受け木、単語のリストを生成

    Args:
        mscx_path (str): MusicXMLのパス
        tstree_path (str): タイムスパン木のパス
        parser (grammar_parser.GrammarParser): 文法の分析に使用する
        mode (int): 単語の一致率か類似度かどちらを求めるかを選択する

    Returns:
        list: タイムスパン木(1番目)、係り受け木(2番目)、単語のリスト(3番目)
    """

    lyrics_notes_dict = lyrics_extractor.extract_lyrics(mscx_path)

    doc = parser.parse(lyrics_notes_dict[lyrics_extractor.LYRICS_KEY])
    lyrics_tree = parser.to_tree(doc)

    words_notes_dict = {}
    explore_words_in_tree(lyrics_tree, words_notes_dict)
    words_list = associate_word_list_notes(words_notes_dict, lyrics_notes_dict)

    tstree = time_span_tree.tstree_xml_2_struct(tstree_path)

    if mode == TREE_SIMILARITY:
        notes_word_dict = associate_notes_words(words_list)
        associate_tstree_words(tstree, notes_word_dict)
        associate_words_tree_notes(lyrics_tree, words_notes_dict)
        simplify_timespan_tree(tstree)

    return [tstree, lyrics_tree, words_list]