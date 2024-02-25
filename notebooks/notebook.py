import pandas as pd
import japanize_matplotlib
from matplotlib import pyplot as plt

RATE_A = "RateA"
RATE_S = "RateS"

YOUTUBE = 0
SPOTIFY = 1

def preprocess(df, csv_path:str):
    rates = pd.merge(df, pd.read_csv(csv_path), on='song')
    rates = rates.dropna(subset=["numerator_A", "denominator_A", "numerator_S", "denominator_S"])

    rates[RATE_A] = rates.numerator_A / rates.denominator_A
    rates[RATE_S] = rates.numerator_S / rates.denominator_S

    x_max = rates.RateA.max()
    x_min = rates.RateA.min()
    y_max = rates.RateS.max()
    y_min = rates.RateS.min()

    xy_max = max(x_max, y_max)
    xy_max += xy_max / xy_max / 100
    xy_min = min(x_min, y_min)
    xy_min -= xy_min / xy_min / 100

    return (rates, xy_min, xy_max)

def is_youtube_or_spotify(y_or_s: int):
    if y_or_s == YOUTUBE:
         return ["youtube_url"], "youtube_play_times"
    else:
         return ["spotify_id"], ["spotify_popularity"]

def scatter(rates:pd.DataFrame, xy_min:int, xy_max:int, y_or_s: int, xlabel:str, ylabel:str, img_path:str):
    subset, sort_by = is_youtube_or_spotify(y_or_s)

    sorted_rates = rates.dropna(subset=subset).sort_values(sort_by, ascending=False)
    center = len(sorted_rates) // 2
    pop = sorted_rates[:center]
    unpop = sorted_rates[center:]

    plt.scatter(x=RATE_A, y=RATE_S, data=pop, color='blue', label='人気曲')
    plt.scatter(x=RATE_A, y=RATE_S, data=unpop, color='red', label='普通曲')

    plt.xlabel(xlabel, fontsize=15)
    plt.ylabel(ylabel, fontsize=15)
    plt.legend(fontsize=15)
    plt.xlim(xy_min, xy_max)
    plt.ylim(xy_min, xy_max)
    plt.tick_params(labelsize=13)
    plt.minorticks_on()
    plt.grid(which='major', color='gray', linestyle='solid')
    plt.grid(which='minor', color='lightgray', linestyle='dotted')
    plt.savefig(img_path)

def preparing_ttest(rates: pd.DataFrame, y_or_s: int) -> dir:
    subset, sort_by = is_youtube_or_spotify(y_or_s)

    sorted_rates = rates.dropna(subset=subset).sort_values(sort_by, ascending=False)
    center = len(sorted_rates) // 2
    pop = sorted_rates[:center]
    unpop = sorted_rates[center:]

    return {"pop": pop, "unpop": unpop}

def head_tail(
        rates: pd.DataFrame,
        y_or_s: int,
        xlabel: str,
        ylabel: str,
        head_lim:int = 2,
        tail_lim:int = 2,
        head_label: str = "人気曲",
        tail_label: str = "普通曲",
        head_color: str = "blue",
        tail_color: str = "red", 
        x: str = RATE_A,
        y: str = RATE_S, 
        ):
        subset, sort_by = is_youtube_or_spotify(y_or_s)
        sorted_rates = rates.dropna(subset=subset).sort_values(sort_by, ascending=False)

        plt.scatter(x=x, y=y, data=sorted_rates.head(head_lim), color=head_color, label= head_label),
        plt.scatter(x=x, y=y, data=sorted_rates.tail(tail_lim), color=tail_color, label= tail_label),

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.minorticks_on()
        plt.grid(which='major', color='gray', linestyle='solid')
        plt.grid(which='minor', color='lightgray', linestyle='dotted')
        