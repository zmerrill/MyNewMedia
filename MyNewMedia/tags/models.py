from django.db import models
#from django.conf import settings
#from django.contrib import admin
#from core.models import TimeStampedModel
#from channels.models import Channel

class Tag (models.Model):
    tagName = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.tagName
    
##admin.site.register(Tag)