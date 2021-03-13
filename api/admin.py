from django.contrib import admin
from .models import File, Song, Podcast, AudioBook

# Register your models here.
admin.site.register(File)
admin.site.register(Song)
admin.site.register(Podcast)
admin.site.register(AudioBook)
