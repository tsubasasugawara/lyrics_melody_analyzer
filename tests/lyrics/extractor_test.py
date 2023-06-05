from alm.lyrics.extractor import extractor

def test_extractor():
    e = extractor.LyricsExtractor()
    e.abstract_lyrics("tests/test_file/オレンジ_A1/score.xml")
    print()
    print(e.lyrics_notes_map)

test_extractor()