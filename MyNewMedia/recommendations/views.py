from django.shortcuts import render
from django.contrib.auth.models import User
from channels.models import Channel
from subscriptions.models import Subscription
from tags.models import Tag 
from collections import defaultdict
import random

def loadRecommendations(request):
    if request.user.is_authenticated():
        thisUser = request.user ##Get the user
        subscriptions = Subscription.objects.filter(user = thisUser)
        popTags = defaultdict(int) ## Hopefully a dictionary?
    ##Go through each one and get the tags
        for subChannel in subscriptions:
            #taglist = subChannel.channel.tags
            #taglist.split(str=",")
            #tagList = subChannel.channel.tags.all#.split(",")
            for sTag in subChannel.channel.tags.all():
                popTags[sTag.name] += 1
    ##Sort by frequency
        sorted(popTags, key=popTags.get)
    ##Get the top 5 or so
        usersTags = popTags.keys()[0:4]
    ##So... for these tags, get some channels
        recChannels = []
        for sTag in usersTags:
            taggedChannels = Channel.objects.filter(tags__name__in=[sTag])
            if len(taggedChannels) > 0:
                try:
                    aChannel = taggedChannels[random.randint(0,len(taggedChannels) - 1)]
                except ValueError:
                    aChannel = taggedChannels[0]
                recChannels.append(aChannel)
            #else: #We couldn't find a channel for that tag; skip it
            #    recChannels.append({'title' : sTag})
    else:
        recChannels = 'NoRecommendations'
    return recChannels
    ##return render(request, "dashboard/user-home.html", {"recommendations": recChannels})
    
        
    