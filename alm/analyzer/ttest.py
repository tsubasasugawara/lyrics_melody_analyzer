import pandas as pd
import numpy as np
from scipy import stats

def ttest_word_matched_rate(csv_path: str):
    df = pd.read_csv(csv_path).dropna(how='any')
    center = len(df) // 2

    MATCHED_RATE_A = "matched_rate_A"
    MATCHED_RATE_S = "matched_rate_S"

    df[MATCHED_RATE_A] = df["matched_word_count_A"] / df["word_count_A"]
    df[MATCHED_RATE_S] = df["matched_word_count_S"] / df["word_count_S"]

    # Youtubeの再生回数でソートしt検定を行う
    sort_by_youtube = df.sort_values("youtube_play_times", ascending=False)
    pop_youtube = sort_by_youtube[:center]
    unpop_youtube = sort_by_youtube[center:]
    pop_youtube_distance = np.abs(pop_youtube[MATCHED_RATE_S] - pop_youtube[MATCHED_RATE_A]) / np.sqrt(2)
    unpop_youtube_distance = np.abs(unpop_youtube[MATCHED_RATE_S] - unpop_youtube[MATCHED_RATE_A]) / np.sqrt(2)
    ttest_youtube = stats.ttest_ind(pop_youtube_distance, unpop_youtube_distance, equal_var=False, alternative='two-sided')

    # Spotifyのpopularityでソートしt検定を行う
    sort_by_spotify = df.sort_values("spotify_popularity", ascending=False)
    pop_spotify = sort_by_spotify[:center]
    unpop_spotify = sort_by_spotify[center:]
    pop_spotify_distance = np.abs(pop_spotify[MATCHED_RATE_S] - pop_spotify[MATCHED_RATE_A]) / np.sqrt(2)
    unpop_spotify_distance = np.abs(unpop_spotify[MATCHED_RATE_S] - unpop_spotify[MATCHED_RATE_A]) / np.sqrt(2)
    ttest_spotify = stats.ttest_ind(pop_spotify_distance, unpop_spotify_distance, equal_var=False, alternative='two-sided')

    return (ttest_youtube, ttest_spotify)

def ttest_tree_similarity(csv_path: str):
    df = pd.read_csv(csv_path).dropna(how='any')
    center = len(df) // 2

    TREE_SIMILARITY_A = "tree_similarity_A"
    TREE_SIMILARITY_S = "tree_similarity_S"

    df[TREE_SIMILARITY_A] = df["matched_subtree_count_A"] / df["subtree_combination_count_A"]
    df[TREE_SIMILARITY_S] = df["matched_subtree_count_S"] / df["subtree_combination_count_S"]

    # Youtubeの再生回数でソートしt検定を行う
    sort_by_youtube = df.sort_values("youtube_play_times", ascending=False)
    pop_youtube = sort_by_youtube[:center]
    unpop_youtube = sort_by_youtube[center:]
    pop_youtube_distance = np.abs(pop_youtube[TREE_SIMILARITY_S] - pop_youtube[TREE_SIMILARITY_A]) / np.sqrt(2)
    unpop_youtube_distance = np.abs(unpop_youtube[TREE_SIMILARITY_S] - unpop_youtube[TREE_SIMILARITY_A]) / np.sqrt(2)
    ttest_youtube = stats.ttest_ind(pop_youtube_distance, unpop_youtube_distance, equal_var=False, alternative='two-sided')

    # Spotifyのpopularityでソートしt検定を行う
    sort_by_spotify = df.sort_values("spotify_popularity", ascending=False)
    pop_spotify = sort_by_spotify[:center]
    unpop_spotify = sort_by_spotify[center:]
    pop_spotify_distance = np.abs(pop_spotify[TREE_SIMILARITY_S] - pop_spotify[TREE_SIMILARITY_A]) / np.sqrt(2)
    unpop_spotify_distance = np.abs(unpop_spotify[TREE_SIMILARITY_S] - unpop_spotify[TREE_SIMILARITY_A]) / np.sqrt(2)
    ttest_spotify = stats.ttest_ind(pop_spotify_distance, unpop_spotify_distance, equal_var=False, alternative='two-sided')

    return (ttest_youtube, ttest_spotify)