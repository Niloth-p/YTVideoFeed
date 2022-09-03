from django.db import models

# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000, blank=True)
    published_at = models.CharField(max_length=30)
    channel_title = models.CharField(max_length=200)
    thumbnail_default = models.URLField(max_length=200, blank=True)
    thumbnail_medium = models.URLField(max_length=200, blank=True)
    thumbnail_high = models.URLField(max_length=200, blank=True)
