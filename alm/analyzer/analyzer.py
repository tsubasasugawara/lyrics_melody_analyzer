import pandas as pd
import numpy as np
from scipy import stats
from matplotlib import pyplot as plt
import seaborn as sns
import math
import japanize_matplotlib
sns.set(font="IPAexGothic")

def show_scatter(popularity: pd.DataFrame, center: int, title: str = "木構造の類似度"):
    pop = popularity[:center]
    unpop = popularity[center:]

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.scatter(pop["類似度_A"], pop["類似度_S"], c='blue')
    ax.scatter(unpop["類似度_A"], unpop["類似度_S"], c='red')
    ax.set_title(title)
    ax.set_xlabel('Aメロ')
    ax.set_ylabel('サビ')
    fig.show()

def analyze_tree_similarities(calc_by: str):
    # TODO:パスが決め打ち
    tree_similarities = pd.read_csv(f"csv/tree_similarities_by_{calc_by}.csv")
    popularities = pd.read_csv("csv/popularities.csv")
    tree_similarities = pd.merge(tree_similarities, popularities)

    center = len(tree_similarities) // 2

    tree_similarities["類似度_A"] = tree_similarities["一致した部分木数_A"] / tree_similarities["部分木の総組み合わせ数_A"]
    tree_similarities["類似度_S"] = tree_similarities["一致した部分木数_S"] / tree_similarities["部分木の総組み合わせ数_S"]

    spotify_popularity = tree_similarities.sort_values("Spotify", ascending=False)
    youtube_popularity = tree_similarities.sort_values("Youtube", ascending=False)

    show_scatter(youtube_popularity, center, "木構造の類似度（Youtube）")
    show_scatter(spotify_popularity, center, "木構造の類似度（Spotify）")