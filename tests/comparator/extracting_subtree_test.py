from alm.comparator import extracting_subtree as ES
from alm.utils import io
from alm.node import node
import pprint

def extracting_subtree_test(file_path: str):
    head = node.Node(
        1,
        [
            node.Node(
                2,
                [
                    node.Node(
                        4,
                        [],
                        True
                    ),
                    node.Node(
                        5,
                        [],
                        True
                    )
                ],
                False
            ),
            node.Node(
                3,
                [
                    node.Node(
                        6,
                        [
                            node.Node(
                                8,
                                [],
                                True
                            ),
                            node.Node(
                                9,
                                [],
                                True
                            ),
                        ],
                        False
                    ),
                    node.Node(
                        7,
                        [],
                        True
                    ),
                ],
                False
            )
        ],
        False
    )

    res = ES.extract_subtree(head)
    io.output_json("tests/files/extracting_subtree_test.json", res)
    pprint.pprint(res)

extracting_subtree_test("tests/files/オレンジ/オレンジ_A1_1_TS.xml")