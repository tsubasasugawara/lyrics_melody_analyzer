from alm.comparator import associating_lyrics_melody as LMM
from alm.lyrics import grammar_parser as GP
from alm.lyrics import lyrics_extractor as LE

def associate_words_notes_test(file_path: str):
    lyrics_notes_map = LE.extract_lyrics(file_path)

    parser = GP.GrammarParser("ja_ginza")
    doc = parser.parse(lyrics_notes_map[LE.LYRICS_KEY])
    tree = parser.to_tree_map(doc)

    lyrics_tree = LMM.associate_word_notes(tree, lyrics_notes_map)
    print(lyrics_tree)

associate_words_notes_test("tests/test_file/オレンジ/オレンジ_A1.xml")
associate_words_notes_test("tests/test_file/オレンジ/オレンジ_S1.xml")