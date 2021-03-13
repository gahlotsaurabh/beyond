from core.serializers import DynamicFieldsModelSerializer
from api.models import File, AudioBook, Song, Podcast


class FileSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = File
        fields = ('__all__')


class AudioBookSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = AudioBook
        fields = ('__all__')


class PodcastSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Podcast
        fields = ('__all__')


class SongSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Song
        fields = ('__all__')
