from django.db import models
from django.conf import settings
from django.contrib import admin
from core.models import TimeStampedModel

class ChannelType(TimeStampedModel):
    type = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.type

class Channel(TimeStampedModel):
    title = models.CharField(max_length=256)
    url_ext = models.CharField(max_length=50, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    description = models.TextField()
    type = models.ForeignKey(ChannelType)
    language = models.CharField(max_length=100)
    feed = models.URLField()
    
    def __unicode__(self):
        return self.title
    
class Link(TimeStampedModel):
    title = models.CharField(max_length=256)
    channel = models.ForeignKey(Channel)
    description = models.TextField()
    url = models.CharField(max_length=256)
    
    def __unicode__(self):
        return self.title
    
admin.site.register(Channel)
admin.site.register(ChannelType)
admin.site.register(Link)

    
