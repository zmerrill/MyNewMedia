from django.db import models
from django.conf import settings
from django.contrib import admin
from core.models import TimeStampedModel
from tags.models import Tag

class ChannelType(TimeStampedModel):
    type = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.type

class Channel(TimeStampedModel):
    title = models.CharField(max_length=256)
    url_ext = models.CharField(max_length=50, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    description = models.TextField(blank=True)
    type = models.ForeignKey(ChannelType)
    language = models.CharField(max_length=100, blank=True)
    feed = models.URLField(blank=True)
    image = models.ImageField("Channel Pic", upload_to="images/", blank=True, null=True)
    tags = models.ManyToManyField(Tag)
    
    def __unicode__(self):
        return self.title
    
class Link(TimeStampedModel):
    title = models.CharField(max_length=256)
    channel = models.ForeignKey(Channel)
    description = models.TextField(blank=True)
    url = models.CharField(max_length=256)
    
    def __unicode__(self):
        return self.title
    
admin.site.register(Channel)
admin.site.register(ChannelType)
admin.site.register(Link)

    
