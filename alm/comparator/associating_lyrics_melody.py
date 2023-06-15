from ..lyrics import lyrics_extractor as LE

def associate_word_notes(lyrics_tree: dict, lyrics_notes_map: dict) -> dict:
    """単語と音符を対応付ける

    Args:
        lyrics_tree (dict): GrammarParserクラスで出力された歌詞の木
        lyrics_notes_map (dict): LyricsExtractorクラスで出力された音符と歌詞の対応を示したリスト
    
    Returns:
        dict: 音符を対応付けた構文解析木
    """

    words_notes_map = {}
    explore_words_in_tree(lyrics_tree, words_notes_map)

    associate_word_list_notes(words_notes_map, lyrics_notes_map)
    associate_words_tree_notes(lyrics_tree, words_notes_map)

    return lyrics_tree

def associate_word_list_notes(words_notes_map: dict, lyrics_notes_map: dict) -> list:
    """単語のリストに音符を対応付ける

    Args:
        words_notes_map (dict): 分割された単語を格納する配列
        lyrics_notes_map (dict): LyricsExtractorクラスで出力された音符と歌詞の対応を示したリスト

    Returns:
        list: 音符を対応付けた単語のリスト
    """

    key_list = sorted(words_notes_map)
    index_words_map_key_list = 0

    chars = ""
    notes = []
    for index_lyrics_map in range(0, len(lyrics_notes_map[LE.CHAR_NOTES_KEY])):
        if index_words_map_key_list >= len(key_list):
            break

        key = key_list[index_words_map_key_list]
        word = words_notes_map[key]["word"]

        chars = chars + lyrics_notes_map[LE.CHAR_NOTES_KEY][index_lyrics_map][LE.CHAR_KEY]
        notes.extend(lyrics_notes_map[LE.CHAR_NOTES_KEY][index_lyrics_map][LE.NOTES_KEY])
        notes = list(dict.fromkeys(notes))

        if word == chars:
            words_notes_map[key]["notes"] = notes
            index_words_map_key_list += 1

            notes = []
            chars = ""
        
    return words_notes_map

def explore_words_in_tree(tree: dict, words_notes_map: dict) -> None:
    """構文解析木から単語を探索し、単語リストを作成する

    Args:
        tree (dict): 構文解析木の部分木
        words_notes_map (dict): 分割された単語を格納する配列
    """

    word = tree["word"]
    number = tree["number"]

    words_notes_map[number] = {"word": word, "notes": []}

    for child in tree["children"]:
        explore_words_in_tree(child, words_notes_map)

def associate_words_tree_notes(tree: dict, words_notes_map: dict) -> None:
    """単語の木に音符を対応付ける

    Args:
        tree (dict): 構文解析木の部分木
        words_notes_map (dict): 単語ごとに音符と対応付けされたマップ
    """

    number = tree["number"]
    tree["notes"] = words_notes_map[number]["notes"]
    # notesとchildrenの順番を入れ替えるために、childrenを再度入れ直す
    tree["children"] = tree.pop("children")

    for child in tree["children"]:
        associate_words_tree_notes(child, words_notes_map)
