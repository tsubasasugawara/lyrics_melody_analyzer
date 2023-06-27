from alm.comparator import extracting_subtree as ES
from alm.utils import util
import pprint

def extracting_subtree_test(file_path: str):
    tree = {
        "id": 1,
        "children": [
            {
                "id": 2,
                "children": [
                    {
                        "id": 4,
                        "children": []
                    },
                    {
                        "id": 5,
                        "children": []
                    }
                ]
            },
            {
                "id": 3,
                "children": [
                    {
                        "id": 6,
                        "children": [
                            {
                                "id": 8,
                                "children": []
                            },
                            {
                                "id": 9,
                                "children": []
                            }
                        ]
                    },
                    {
                        "id": 7,
                        "children": []
                    },
                ]
            }
        ]
    }
    res = ES.extract_subtree(tree)
    util.output_json("tests/files/extracting_subtree_test.json", res)
    pprint.pprint(res)

extracting_subtree_test("tests/files/オレンジ/オレンジ_A1_1_TS.xml")