"""Fetches the latest videos for a given topic, in the background"""
import json
import os
import requests

from videoFeeder import settings


def get_last_time():
    """Find the time the latest video in our DB was published"""
    search_url = "http://127.0.0.1:8000/" + os.environ['TOPIC'] + '/'
    resp = requests.get(search_url, timeout=10)
    if(len(resp.json()['results'])) == 0:
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
        'key': os.environ['YOUTUBE_DATA_API_KEY']
    }

    try:
        response = requests.get(search_url, params=params, timeout=10)
        response.raise_for_status()
        vids = response.json()['items']
        save_details(vids, last_time)
    except requests.HTTPError as e:
        print(e)


def save_details(vids, last_time):
    """Save the video details to the DB"""
    for vid in vids:
        if last_time == vid['snippet']['publishedAt']:
            continue
        search_url = 'http://127.0.0.1:8000/' + os.environ['TOPIC'] + '/'
        vid_id = vid['id']['videoId']
        vid = vid['snippet']
        data = {
            'title': vid['title'],
            'url': 'https://www.youtube.com/watch?v=' + vid_id,
            'description': vid['description'],
            'published_at': vid['publishedAt'],
            'channel_title': vid['channelTitle'],
            'thumbnail_default': vid['thumbnails']['default']['url'],
            'thumbnail_medium': vid['thumbnails']['medium']['url'],
            'thumbnail_high': vid['thumbnails']['high']['url'],
        }
        _resp = requests.post(search_url, data=data, timeout=10)


if __name__ == '__main__':
    fetch_videos()
