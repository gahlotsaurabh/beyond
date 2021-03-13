from core.models import BaseContent
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation


FILE_TYPE = [
    ("SONG", 'SONG'),
    ("PODCAST", 'PODCAST'),
    ("AUDIOBOOK", 'AUDIOBOOK')
]


class File(BaseContent):
    file = models.FileField(upload_to='', null=True)
    _type = models.CharField(
        choices=FILE_TYPE, default="Product", max_length=250
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self):
        return "%s - %s" % (self.file, self.id)

    # @property
    # def prop(self):


class Song(BaseContent):
    name = models.CharField(max_length=100)
    Duration = models.IntegerField()
    file = GenericRelation(File, related_query_name='song')

    def __str__(self):
        return "%s - %s" % (self.name, self.id)


class Podcast(BaseContent):
    name = models.CharField(max_length=100)
    Duration = models.IntegerField()
    host = models.CharField(max_length=100)
    participants = ArrayField(
        models.CharField(max_length=100, blank=True),
        size=10, blank=True
    )
    file = GenericRelation(File, related_query_name='podcast')

    def __str__(self):
        return "%s - %s" % (self.name, self.id)


class AudioBook(BaseContent):
    title = models.CharField(max_length=100)
    Duration = models.IntegerField()
    author = models.CharField(max_length=100)
    Narrator = models.CharField(max_length=100)
    file = GenericRelation(File, related_query_name='audiobook')

    def __str__(self):
        return "%s - %s" % (self.title, self.id)
