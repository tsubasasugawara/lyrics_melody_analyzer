import spacy

def load_ginza():
    nlp = spacy.load('ja_ginza')
    return nlp