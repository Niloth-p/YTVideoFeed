from apscheduler.schedulers.background import BackgroundScheduler
from videoFetcher import videoFetchApi


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(videoFetchApi.fetch_videos, 'interval', minutes=1)
    scheduler.start()
