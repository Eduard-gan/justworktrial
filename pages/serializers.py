from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer, SerializerMethodField
from pages.models import Video, Audio, Text, Page


class VideoSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'counter', 'video_file_link', 'subtitles_file_link']


class AudioSerializer(ModelSerializer):
    class Meta:
        model = Audio
        fields = ['id', 'title', 'counter',  'bit_rate']


class TextSerializer(ModelSerializer):
    class Meta:
        model = Text
        fields = ['id', 'title', 'counter',  'body']


class PageDetailSerializer(ModelSerializer):
    contents = SerializerMethodField()

    class Meta:
        model = Page
        fields = ['id', 'title', 'contents']

    def get_videos(self, instance):
        videos = instance.videos.all().order_by('id')
        return VideoSerializer(videos, many=True).data

    def get_audios(self, instance):
        audios = instance.audios.all().order_by('id')
        return AudioSerializer(audios, many=True).data

    def get_texts(self, instance):
        texts = instance.texts.all().order_by('id')
        return TextSerializer(texts, many=True).data

    def get_contents(self, instance):
        videos = self.get_videos(instance)
        audios = self.get_audios(instance)
        texts = self.get_texts(instance)
        return videos + audios + texts


class PageListSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Page
        fields = ('id', 'title', 'url')
