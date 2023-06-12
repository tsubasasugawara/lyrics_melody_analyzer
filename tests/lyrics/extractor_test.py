from alm.lyrics import lyrics_extractor as lec

def test_extractor(file_path: str):
    lyrics_notes_map = lec.abstract_lyrics(file_path)
    print(lyrics_notes_map)

test_extractor("tests/test_file/オレンジ/オレンジ_S1.xml")