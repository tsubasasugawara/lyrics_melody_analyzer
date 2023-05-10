from spacy import displacy
from . import util
from . import load_model

def parse(in_dir_path, out_dir_path, artist):
    # 文法構造を解析
    res = parse_file(f"{util.put_slash_dir_path(in_dir_path)}{artist}.json")

    # 文法構造の可視化
    for song_name in res["songs"]:
        visualize(res["songs"][song_name], song_name)
    
    # 曲ごとの構文木のJSONファイルを出力
    for song_name in res["songs"]:
        data = to_tree_map(artist, res["songs"][song_name])

        out_dir_path = util.put_slash_dir_path(out_dir_path)
        util.make_dir(out_dir_path)

        util.output_json(f"{out_dir_path}{song_name}.json", data)

#　文法構造を解析する
def parse_file(file_path):
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
    node = {"word": token.text, "number": token.i, "children": {}}

    node["children"] = []
    for child in token.children:
        node["children"].append(recur_tree(child))

    return node

# 根を結合する
def join_roots(roots):
    if len(roots) <= 1:
        return roots

    res = roots[0]
    for i in range(1,len(roots)):
        if len(res["children"]) > len(roots[i]["children"]):
            temp = roots[i]
            temp["children"].append(res)
            res = temp
        else:
            res["children"].append(roots[i])
    return res


# 文法構造をもとに、構文木のJSONファイルを作成する
def to_tree_map(artist, song):
    data = {}
    for section in song:
        data[section] = []
        for sent in song[section].sents:
            data[section].append(recur_tree(sent.root))

        data[section] = join_roots(data[section])
    
    return data
    
        