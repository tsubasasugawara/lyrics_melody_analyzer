import spacy

def load_ginza() -> spacy.Language:
    """GiNZAの読み込み

    Returns:
        spacy.Language: 読み込んだもの
    """

    nlp = spacy.load('ja_ginza')
    return nlp