import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import time

class Track:
    def __init__(self, name: str, popularity: str) -> None:
        """トラック情報

        Args:
            name (str): トラック名
            popularity (str): 人気度
        """

        self.name = name
        self.popularity = popularity

def get_popularities(track_id_list: list) -> list:
    client_id = os.environ["SPOTIFY_CLIENT_ID"]
    client_secret = os.environ["SPOTIFY_SECRET"]
    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)

    res = []
    for track_id in track_id_list:
        track = get_track(track_id, client_credentials_manager)
        time.sleep(3)
        if type(track) is dict:
            res.append([track["name"], track["popularity"]])
    
    return res

def get_popularity(track_id: str) -> (Track | None):
    """人気度を取得する

    Args:
        track_id (str): トラックID

    Returns:
        (Track | None): トラック情報を取得できたらTrack型のデータを返す
    """

    client_id = os.environ["SPOTIFY_CLIENT_ID"]
    client_secret = os.environ["SPOTIFY_SECRET"]
    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    
    track = get_track(track_id, client_credentials_manager)

    if type(track) is dict:
        return Track(track["name"], track["popularity"])
    else:
        return None

def get_track(track_id: str, client_credentials_manager: SpotifyClientCredentials) -> (dict | None):
    """トラック情報を取得する

    Args:
        track_id (str): トラックID

    Returns:
        (dict | None): トラック情報を取得できたときに辞書型配列を返す
    """

    spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager, language="ja")

    try:
        res = spotify.track(track_id, market="JP")
        return res
    except:
        return None