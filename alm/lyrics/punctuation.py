import spacy
from ..utils import util

#TODO: クラス
#TODO: テスト
def add_punctuation(nlp: spacy.Language, text: str) -> str:
    """句読点を追加

    Args:
        nlp (spacy.Language): モデルを読み込んだもの
        text (str): 句読点を追加したい文字列

    Returns:
        str: 句読点を追加した文字列
    """

    doc = nlp(text)

    res = ""
    pre_token = None

    for sent in doc.sents:
        for token in sent:
            
            if token.text != "\n":
                res = res + token.text

            if pre_token == None:
                pre_token = token
                continue

            pre_morph = pre_token.morph.get("Inflection")

            if token.text == "\n" and pre_token.text != ("!" or "?" or "！" or "？"):
                if (
                    (len(pre_morph) > 0 and util.contains(["連用形", "連体形"], pre_morph[0]))
                    or util.contains(["名詞", "間投詞", "副詞", "接続詞", "感嘆詞"], pre_token.tag_)
                    or ("助詞" in pre_token.tag_ and "終助詞" not in pre_token.tag_)
                    ):
                    res = res + "、"
                else:
                    res = res + "。"

            pre_token = token

    return res