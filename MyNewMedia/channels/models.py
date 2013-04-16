from django.db import models
from django.conf import settings
from django.contrib import admin
from core.models import TimeStampedModel
from taggit.managers import TaggableManager

# Channel type model
# Contains admin defined list of channel types
class ChannelType(TimeStampedModel):
    type = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.type

# Channel model
class Channel(TimeStampedModel):
    # Channel title
    title = models.CharField(max_length=256)
    # URL Extension used for browser navigation
    url_ext = models.CharField(max_length=50, unique=True)
    # Foreign key to the user who created the channel
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    # Description of the channel content
    description = models.TextField(blank=True)
    # Channel type - foreign key to ChannelType table
    type = models.ForeignKey(ChannelType)
    # Language the channel is in
    language = models.CharField(max_length=100, blank=True)
    # URL the channel will pull the RSS feed XML document from
    feed = models.URLField(blank=True)
    # Channel picture displayed with all instances of a channel
    image = models.ImageField("Channel Pic", upload_to="images/", blank=True, null=True)
    # Set of tags describing the channel
    tags = TaggableManager()
    
    # Descriptor - think java toString()
    def __unicode__(self):
        return self.title

# Link model    
class Link(TimeStampedModel):
    # Link title
    title = models.CharField(max_length=256)
    # Foreign key to the channel the link belongs to
    channel = models.ForeignKey(Channel)
    # Description of the link
    description = models.TextField(blank=True)
    # URL pointing to content
    url = models.CharField(max_length=256)
    
    def __unicode__(self):
        return self.title
    
# Individual record of an RSS feed. Contains all items
# from an RSS field. Used to create user history
class FeedItem(TimeStampedModel):
    # Title of the item
    title = models.CharField(max_length=1000)
    # Channel the item belongs to
    channel = models.ForeignKey(Channel)
    # The link to the item
    link = models.URLField()
    # The count within the channel - NOT UNIQUE ACROSS
    # CHANNELS!!!
    itemcount = models.IntegerField()
    
    def __unicode__(self):
        return self.title

# FeedTracker model contains actual user watch history
class FeedTracker(TimeStampedModel):
    # Feed item viewed
    item = models.ForeignKey(FeedItem)
    # User who viewed the item
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    # Channel the item belongs to
    channel = models.ForeignKey(Channel)
    
# Registers all models to the admin site
admin.site.register(Channel)
admin.site.register(ChannelType)
admin.site.register(Link)
admin.site.register(FeedItem)
admin.site.register(FeedTracker)

    
