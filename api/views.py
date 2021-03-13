from api.models import File, Podcast, Song, AudioBook
from api.serializers import (
        FileSerializer, SongSerializer, AudioBookSerializer,
        PodcastSerializer
    )
from rest_framework import viewsets
import os
import sys
from core.renderers import Response
from rest_framework import status
import mutagen


class FileViewSet(viewsets.ModelViewSet):
    """
    queryparam for file type === /?_type=
    file = {file, _type}
    song = {name}
    podcast = {name, host, participants}
    audiobook = {title, author, Narrator}
    based on the file type add data in payload
    payload = {
        file,
        _type,
        name,
        host,
        participants,
        title,
        author,
        Narrator
    }
    query param : _type
    """
    queryset = File.objects.all()
    serializer_class = FileSerializer

    class Meta:
        ordering = ['-id']

    def get_queryset(self):
        if self.request.query_params.get('_type', None):
            return self.queryset.filter(
                _type=self.request.query_params.get('_type')
            ).order_by('-id')
        return self.queryset

    def get_serializer1(self, _type):
        if _type == "SONG":
            return SongSerializer
        if _type == "AUDIOBOOK":
            return AudioBookSerializer
        if _type == "PODCAST":
            return PodcastSerializer

    def get_related_obj(self, _type, obj):
        if _type == "SONG":
            return Song.objects.filter(file=obj).first()
        if _type == "AUDIOBOOK":
            return AudioBook.objects.filter(file=obj).first()
        if _type == "PODCAST":
            return Podcast.objects.filter(file=obj).first()

    def create(self, request, pk=None):
        """
        """
        status_ = status.HTTP_500_INTERNAL_SERVER_ERROR
        message = "Internal server error"
        data = {}
        try:
            file = FileSerializer(data=request.data, fields=('_type', 'file'))
            audio_info = mutagen.File(request.data.get("file")).info
            payload = request.data
            if not file.is_valid():
                status_ = status.HTTP_400_BAD_REQUEST
                message = "Bad Request"
                return Response(data, data_status=status_, message=message)

            payload['Duration'] = int(audio_info.length)
            if request.data.get("_type") is not None:
                if request.data.get("_type") == "PODCAST" and\
                        request.data.get("participants") is None:
                    payload['participants'] = ""

                serilizer = self.get_serializer1(
                    request.data.get("_type")
                )(data=payload, fields=payload.keys())
                if serilizer.is_valid(raise_exception=True):
                    serilizer = serilizer.save()
                    serilizer.file.create(
                        file=request.data.get("file"),
                        _type=request.data.get("_type")
                    )
            status_ = status.HTTP_200_OK
            message = ""
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(str(e))
        return Response(data, data_status=status_, message=message)

    def partial_update(self, request, pk=None):
        """
        payload = {
                file,
                _type,
                name,
                host,
                participants,
                title,
                author,
                Narrator
            }
        """
        status_ = status.HTTP_500_INTERNAL_SERVER_ERROR
        message = "Internal server error"
        data = {}
        # geting obj from id
        obj = self.get_object()
        rel_obj = self.get_related_obj(request.data.get("_type"), obj)
        try:
            if rel_obj is None or request.data.get("_type") is None:
                status_ = status.HTTP_400_BAD_REQUEST
                message = "Bad Request"
                return Response(data, data_status=status_, message=message)

            # setting payload
            payload = request.data
            file = request.data.get("file") if request.data.get("file")\
                is not None else obj.file
            audio_info = mutagen.File(file).info
            payload['Duration'] = int(audio_info.length)

            # updating relation obj
            serilizer = self.get_serializer1(
                request.data.get("_type")
            )(rel_obj, data=payload, partial=True)

            if serilizer.is_valid(raise_exception=True):
                serilizer.save()
                if request.data.get("file"):
                    # updating file obj
                    obj.file = request.data.get("file")
                    obj._type = request.data.get("_type")
                    obj.save()
            status_ = status.HTTP_200_OK
            message = ""
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(str(e))
        return Response(data, data_status=status_, message=message)
