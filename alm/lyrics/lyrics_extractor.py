import xml.etree.ElementTree as et

CHAR_NOTES_KEY = "char_notes"
MEASURES_KEY = "measures"
LYRICS_KEY = "lyrics"
CHAR_KEY = "char"
NOTES_KEY = "notes"
CHAR_NUMBER = "char_number"

def extract_lyrics(file_path: str) -> dict:
    """MusicXmlから歌詞を抽出して音符と対応付ける

    Args:
        file_path (str): 歌詞を抽出したファイルのパス

    Returns:
        dict: 歌詞の1文字と音符が対応付けられた辞書
    """

    try:
        tree = et.parse(file_path)
    except et.ParseError as err:
        print("ParseError:", err)
        return

    part = tree.find("part").attrib["id"]

    lyrics_notes_dict = mapping_lyrics_notes(tree.iter("measure"), part)

    return split_char(lyrics_notes_dict)

def mapping_lyrics_notes(measures, part: str) -> dict:
    """歌詞を抽出し、音符と対応付ける

    Args:
        measures (Any): xmlからiter関数によって抜き出したmeasureタグのリスト
        part: 小節ID
    
    Returns:
        dict: 歌詞と音符を対応付けた辞書
    """

    lyrics_notes_dict = {CHAR_NOTES_KEY: [], MEASURES_KEY: [], LYRICS_KEY: ""}
    
    char= ''
    lyrics = ""
    tie_note_id = ""
    for measure in measures:
        measure_number = measure.attrib["number"]
        measure_lyrics = ""
        notes_cnt = 0
        is_prev_rest = False # 前に休符があるかどうか

        for note in measure.iter("note"):
            notes_cnt += 1

            # 休符かどうかを確認し、前も休符の場合はnotes_cntを-1することでIDを正しく付ける
            rest = note.find("rest")
            if rest != None and is_prev_rest:
                notes_cnt -= 1
            if rest != None:
                is_prev_rest = True
                continue
            is_prev_rest = False

            # タイの後ろの音符の場合は、前と同じIDにする
            tie_list = note.findall("tie")
            if len(tie_list) > 1:
                note_id = tie_note_id
            elif len(tie_list) == 1 and tie_list[0].attrib["type"] == "stop":
                note_id = tie_note_id
            else:
                note_id = '-'.join([part, measure_number, str(notes_cnt)])
            
            if len(tie_list) == 1 and tie_list[0].attrib["type"] == "start":
                tie_note_id = note_id

            # 歌詞を抜き出し、音符と対応付ける
            lyric_ele = note.find("lyric")
            if lyric_ele != None:
                char= lyric_ele.find("text").text

                # XMLから抜き出したときに、半角スペースが\xa0となるため、それを戻す
                char = char.replace("\xa0", " ")

                measure_lyrics = measure_lyrics + char
                lyrics = lyrics + char

                lyrics_notes_dict[CHAR_NOTES_KEY].append({CHAR_KEY: char, NOTES_KEY: [note_id]})
                lyrics_notes_dict[CHAR_NOTES_KEY][-1][CHAR_NUMBER] = len(lyrics_notes_dict[CHAR_NOTES_KEY]) - 1
            else:
                lyrics_notes_dict[CHAR_NOTES_KEY][-1][NOTES_KEY].append(note_id)
            
        # 小節ごとの歌詞を辞書型配列に追加する
        lyrics_notes_dict[MEASURES_KEY].append(measure_lyrics)

    lyrics_notes_dict[LYRICS_KEY] = lyrics 
    return lyrics_notes_dict

def split_char(lyrics_notes_dict: dict) -> dict:
    """一つの音符に2文字以上が対応しているときに分割する

    Args:
        lyrics_notes_dict (dict): 歌詞と音符を対応付けた辞書

    Returns:
        dict: 1文字ごとに音符と対応付けた辞書型
    """

    index = 0
    while True:
        if index >= len(lyrics_notes_dict[CHAR_NOTES_KEY]) - 1:
            break

        chars = lyrics_notes_dict[CHAR_NOTES_KEY][index][CHAR_KEY]
        chars = chars.replace(" ", "")

        char_list = list(chars)
        if len(char_list) <= 1:
            index += 1
            continue

        char_notes = lyrics_notes_dict[CHAR_NOTES_KEY][index]
        lyrics_notes_dict[CHAR_NOTES_KEY].pop(index)
        for i in range(len(char_list)):
            lyrics_notes_dict[CHAR_NOTES_KEY].insert(index + i, {CHAR_KEY: char_list[i], NOTES_KEY: char_notes[NOTES_KEY], CHAR_NUMBER: char_notes[CHAR_NUMBER]})

        index += len(char_list)
    
    return lyrics_notes_dict
