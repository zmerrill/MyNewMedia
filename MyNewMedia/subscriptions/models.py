from django.db import models
from django.conf import settings
from django.contrib import admin
from core.models import TimeStampedModel
from channels.models import Channel

# Basic subscrition model -
# Foreign keys to the user and channel relationship
# Number of unread posts
class Subscription(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    channel = models.ForeignKey(Channel)
    unread = models.IntegerField()
    
    def __unicode__(self):
        return '%s : %s' % (self.user, self.channel)
    
admin.site.register(Subscription) 
    
    
