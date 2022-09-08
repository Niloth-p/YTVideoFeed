from django.apps import AppConfig


class VideoappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'videoApp'

    def ready(self):
        from videoFetcher import fetcher
        fetcher.start()