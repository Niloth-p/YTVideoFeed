from rest_framework import viewsets, filters

from videoApp.models import Video
from videoApp.serializers import VideoSerializer


# Create your views here.
class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all().order_by('-published_at')
    serializer_class = VideoSerializer
    search_fields = ['title', 'description']
    filter_backends = (filters.SearchFilter, )
