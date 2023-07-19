import json
import glob
from pathlib import Path
import os
from os import path
import csv

XML = "xml"

def read_json(file_path: str) -> dict:
    """JSONファイルを読み込む

    Args:
        file_path (str): ファイルパス

    Returns:
        dict: 辞書型配列で表現されたJSONデータ
    """

    f = open(file_path, 'r', encoding="utf-8")
    data = json.load(f)
    f.close()
    return data

def output_json(file_path: str, data: dict) -> None:
    """JSONファイルを出力する

    Args:
        file_path (str): 出力先のファイルパス
        data (dict): 書き込むデータ
    """

    f = open(file_path, 'w+', encoding="utf-8")
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.close()

def output_csv(file_path: str, header: list, data: list) -> None:
    """CSV形式で出力

    Args:
        file_path (str): 出力先のファイルパス
        data (list): 書き込むデータ
    """

    f = open(file_path, 'w+', encoding='utf-8')
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data)
    f.close()

def put_slash_dir_path(dir_path) -> str:
    """パスの最後にスラッシュを追加する

    Args:
        dir_path (_type_): パス

    Returns:
        str: スラッシュ追加後のパス
    """

    if dir_path[-1] != "/":
        dir_path = dir_path + "/"
    return dir_path

def get_file_list(dir_path: str, extension: str) -> list:
    """ファイルの一覧を取得

    Args:
        dir_path (str): 一覧を取得したいディレクトリのパス
        extension (str): 拡張子

    Returns:
        list: ファイル一覧
    """

    if len(dir_path) <= 0:
        return []
    
    path = put_slash_dir_path(dir_path) + f"*.{extension}"
    
    return glob.glob(path);

def get_file_name(file_path: str) -> str:
    """ファイル名を取得する

    Args:
        file_path (str): ファイルパス

    Returns:
        str: ファイル名
    """

    return Path(file_path).stem

def make_dir(dir_path: str) -> None:
    """ディレクトリを作成する

    Args:
        dir_path (str): ディレクトリを作る先のパス
    """

    if path.exists(dir_path) == False:
        os.makedirs(dir_path)

