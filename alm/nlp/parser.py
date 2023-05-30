from spacy import displacy
import spacy
from . import util
from . import load_model

def parse(in_dir_path: str, out_dir_path: str, artist: str) -> None:
    """文法構造を解析する

    係り受け木を可視化する
    JSONファイルに木を保存する

    Args:
        in_dir_path (str): 入力ファイルがあるディレクトリパス
        out_dir_path (str): 出力先のディレクトリパス
        artist (str): アーティスト名
    """

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

def parse_file(file_path: str) -> dict:
    """文法構造を解析し、辞書型配列として返す

    Args:
        file_path (str): 解析対象のファイルパス

    Returns:
        dict: 解析結果の辞書型配列
    """
    
    songs = util.read_json(file_path)
    nlp = load_model.load_ginza()
    
    res = {"artist": util.get_file_name(file_path), "songs": {}}

    for song in songs:
        res["songs"][song] = {}
        for section in songs[song]:
            res["songs"][song][section] = nlp(songs[song][section])

    return res

#TODO: 曲名を引数で受取り、解析結果から検索して表示したほうが良いのでは？(クラスにしてしまったほうが良い可能性)
def visualize(song: dict, song_name: str) -> None:
    """歌詞の文法構造を可視化する

    Args:
        song (dict): 解析結果のある1曲
        song_name (str): 曲名
    """

    for section in song:
        print(song_name, section, "\n")
        displacy.render(song[section], style='dep', jupyter=True, options={'compact':True, 'distance': 90})

def recur_tree(token: spacy.Token) -> dict:
    """再帰的に木を作成する

    Args:
        token (spacy.Token): 解析結果のトークン

    Returns:
        dict: 木のノード
    """

    node = {"word": token.text, "number": token.i, "children": {}}

    node["children"] = []
    for child in token.children:
        node["children"].append(recur_tree(child))

    return node

def join_roots(roots: list) -> dict:
    """ルートが複数ある場合に結合する

    Args:
        roots (list): ルートのリスト

    Returns:
        dict: 結合後の木
    """

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

#TODO: 解析結果のための構造体を作る
def to_tree_map(song: dict) -> dict:
    """係り受け木を辞書型にする

    Args:
        song (dict): ある曲の解析結果

    Returns:
        dict: 辞書型配列として表現された係り受け木
    """
    data = {}
    for section in song:
        data[section] = []
        for sent in song[section].sents:
            data[section].append(recur_tree(sent.root))

        data[section] = join_roots(data[section])
    
    return data
    
        