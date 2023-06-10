from alm.lyrics.extractor import lyrics_extractor

def test_extractor():
    e = lyrics_extractor.LyricsExtractor()
    e.abstract_lyrics("tests/test_file/オレンジ/オレンジ_S1.xml")
    print()
    print(e.lyrics_notes_map)

test_extractor()