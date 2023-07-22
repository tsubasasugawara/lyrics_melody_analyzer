from alm.comparator import extracting_subtree as ES
from alm.lyrics import *
from alm.melody import *
from alm.utils import io
from alm.node import node
import pprint

def extracting_parent_child_test(mscx_path: str, tstree_path: str):
    parser = grammar_parser.GrammarParser("ja_ginza")
    lyrics_notes_map = lyrics_extractor.extract_lyrics(mscx_path)
    doc = parser.parse(lyrics_notes_map[lyrics_extractor.LYRICS_KEY])
    lyrics_tree = parser.to_tree(doc)

    tstree = time_span_tree.tstree_xml_2_struct(tstree_path)

    pprint.pprint(ES.extract_parent_child(lyrics_tree))
    print()
    pprint.pprint(ES.extract_parent_child(tstree))

extracting_parent_child_test("xmls/pop/BE_FREE_A.xml", "xmls/pop_tstree/BE_FREE_A_TS.xml")
