import pandas as pd
import numpy as np
from scipy import stats

def ttest_word_matched_rate(word_matched_rate_csv_path: str, popularities_csv_path: str):
    word_matched_rate = pd.read_csv(word_matched_rate_csv_path)
    popularities = pd.read_csv(popularities_csv_path)
    merged_data = pd.merge(word_matched_rate, popularities)
    center = len(merged_data) // 2

    MATCHED_RATE_A = "一致率_A"
    MATCHED_RATE_S = "一致率_S"

    merged_data[MATCHED_RATE_A] = merged_data["一致した単語数_A"] / merged_data["単語数_A"]
    merged_data[MATCHED_RATE_S] = merged_data["一致した単語数_S"] / merged_data["単語数_S"]

    # Youtubeの再生回数でソートしt検定を行う
    sort_by_youtube = merged_data.sort_values("Youtube", ascending=False)
    pop_youtube = sort_by_youtube[:center]
    unpop_youtube = sort_by_youtube[center:]
    pop_youtube_distance = np.abs(pop_youtube["一致率_S"] - pop_youtube["一致率_A"]) / np.sqrt(2)
    unpop_youtube_distance = np.abs(unpop_youtube["一致率_S"] - unpop_youtube["一致率_A"]) / np.sqrt(2)
    ttest_youtube = stats.ttest_ind(pop_youtube_distance, unpop_youtube_distance, equal_var=False, alternative='two-sided')

    # Spotifyのpopularityでソートしt検定を行う
    sort_by_spotify = merged_data.sort_values("Spotify", ascending=False)
    pop_spotify = sort_by_spotify[:center]
    unpop_spotify = sort_by_spotify[center:]
    pop_spotify_distance = np.abs(pop_spotify["一致率_S"] - pop_spotify["一致率_A"]) / np.sqrt(2)
    unpop_spotify_distance = np.abs(unpop_spotify["一致率_S"] - unpop_spotify["一致率_A"]) / np.sqrt(2)
    ttest_spotify = stats.ttest_ind(pop_spotify_distance, unpop_spotify_distance, equal_var=False, alternative='two-sided')

    return (ttest_youtube, ttest_spotify)