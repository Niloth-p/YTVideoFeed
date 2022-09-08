import os
import requests

from videoApp.models import Video


def get_last_time():
    """Find the time the latest video in our DB was published"""
    search_url = "http://127.0.0.1:8000/" + os.environ['TOPIC'] + '/'
    resp = requests.get(search_url, timeout=10)
    if len(resp.json()['results']) == 0:
        last_time = '2022-06-01T00:00:00Z'
    else:
        last_time = resp.json()['results'][0]['published_at']
    return last_time


def fetch_videos():
    """Get topic related videos from YouTube"""
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    topic = os.environ['TOPIC']

    last_time = get_last_time()
    params = {
        'part': 'snippet',
        'q': topic,
        'type': 'video',
        'publishedAfter': last_time,
        'maxResults': 50,
        'order': 'date',
    }

    keylist = os.environ.get('YOUTUBE_DATA_API_KEYS').split(",")
    i = 0
    fetch_success = 0
    while i < len(keylist) and fetch_success == 0:
        try:
            params['key'] = keylist[i]
            response = requests.get(search_url, params=params, timeout=10)
            response.raise_for_status()
            vids = response.json()['items']
            save_details(vids, last_time)
            fetch_success = 1
        except requests.HTTPError as _e:
            i = i + 1


def save_details(vids, last_time):
    """Save the video details to the DB"""
    for vid in vids:
        if last_time == vid['snippet']['publishedAt']:
            continue
        try:
            new_vid = Video()
            new_vid.url = 'https://www.youtube.com/watch?v=' + vid['id']['videoId']
            vid = vid['snippet']
            new_vid.title = vid['title']
            new_vid.description = vid['description']
            new_vid.published_at = vid['publishedAt']
            new_vid.channel_title = vid['channelTitle']
            new_vid.thumbnail_default = vid['thumbnails']['default']['url']
            new_vid.thumbnail_medium = vid['thumbnails']['medium']['url']
            new_vid.thumbnail_high = vid['thumbnails']['high']['url']
            new_vid.save()
        except:
            print("Unable to save video")
