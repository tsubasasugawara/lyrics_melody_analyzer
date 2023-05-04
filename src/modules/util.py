import json
import glob
from pathlib import Path
import os
from os import path

def read_json(file_path):
    f = open(file_path, 'r', encoding="utf-8")
    data = json.load(f)
    f.close()
    return data

# dataは辞書型のデータ
def output_json(file_path, data):
    f = open(file_path, 'w+', encoding="utf-8")
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.close()

def get_file_list(dir_path):
    if len(dir_path) <= 0:
        return []
    
    if dir_path[-1] != "/":
        dir_path = dir_path + "/"
    path = dir_path + "*.json"
    
    return glob.glob(path);

# 拡張子などを取り除く
def get_file_name(file_path):
    return Path(file_path).stem

def make_dir(dir_path):
    if path.exists(dir_path) == False:
        os.mkdir(dir_path)

# 文字列が含まれるかどうか
def contains(str_list, text):
    res = False
    for s in str_list:
        res = res or s in text
    return res