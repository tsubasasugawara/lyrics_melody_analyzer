from spacy import displacy
from . import util
from . import load_model
import json

#　文法構造を解析する
def parse(file_path):
    songs = util.read_json(file_path)
    nlp = load_model.load_ginza()
    
    res = {"artist": util.get_file_name(file_path), "songs": {}}

    for song in songs:
        res["songs"][song] = {}
        for section in songs[song]:
            res["songs"][song][section] = nlp(songs[song][section])

    return res

# 歌詞の文法構造を可視化する
def visualize(song, song_name):
    for section in song:
        print(song_name, section, "\n")
        displacy.render(song[section], style='dep', jupyter=True, options={'compact':True, 'distance': 90})

# 再帰的に木を作成する
def recur_tree(token):
    node = {"number": token.i, "children": {}}
    for child in token.children:
        node["children"][child.text] = recur_tree(child)
    return node

# 文法構造をもとに、木を作成する
def make_tree(song):
    data = {}
    for section in song:
        data[section] = {}
        for sent in song[section].sents:
            data[section][sent.text] = {}
            data[section][sent.text][sent.root.text] = recur_tree(sent.root)
    
    return data