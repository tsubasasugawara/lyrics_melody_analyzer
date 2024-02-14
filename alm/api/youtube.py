import json
import os
import urllib.parse
from apiclient.discovery import build

API_KEY = os.environ['YOUTUBE_API_KEY']
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def get_video_viewcount(url, api_key):
    qs = urllib.parse.urlparse(url).query
    params = urllib.parse.parse_qs(qs)
    video_id = params['v'][0]

    youtube = build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        developerKey=API_KEY
    )

    res = youtube.videos().list(
        part='snippet, statistics',
        id = video_id
        ).execute()

    items = res.get("items")[0]
    print(items["statistics"]["viewCount"])

get_video_viewcount('https://www.youtube.com/watch?v=ZRtdQ81jPUQ', API_KEY)