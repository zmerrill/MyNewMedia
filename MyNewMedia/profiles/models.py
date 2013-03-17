from django.db import models
from django.conf import settings
from django.contrib import admin
from core.models import TimeStampedModel
from channels.models import ChannelType

class UserProfile(TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    bio = models.TextField()
    location = models.CharField(max_length=256)
    homepage = models.URLField()
    birthday = models.DateField()
    occupation = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    #avatar = models.ImageField("Profile Pic", upload_to="images/", blank=True, null=True)
    page_views = models.IntegerField(default=0)
    def __unicode__(self):
        return unicode(self.owner)
    
class UserPreferences(TimeStampedModel):
    profile = models.ForeignKey(UserProfile)
    type = models.ForeignKey(ChannelType)
    links_per_page = models.IntegerField(default=5)
    
admin.site.register(UserProfile)
admin.site.register(UserPreferences)
    