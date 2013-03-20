from django.shortcuts import render
from channels.models import Channel, ChannelType
from subscriptions.models import Subscription
from profiles.models import UserProfile

def getImage(user):
    try:
        profile = UserProfile.objects.get(owner=user)
        img = "/media/" + profile.avatar.name
    except UserProfile.DoesNotExist:
        profile = None
        img = None
    return img

def index(request):
    if request.user.is_authenticated():
        subscribed = Subscription.objects.filter(user=request.user)
        channels = Channel.objects.filter(owner=request.user)
        img = getImage(request.user)
        
        return render(request, "dashboard/user-home.html", {"subscribed": subscribed, "channels": channels, "user": request.user, "img": img})
    else:
        channels = Channel.objects.all()
        types = ChannelType.objects.all()
        return render(request, "index.html", {"channels": channels, "types": types})
    
def mychannels(request):
    if request.user.is_authenticated():
        subscribed = Subscription.objects.filter(user=request.user)
        channels = Channel.objects.filter(owner=request.user)
        img = getImage(request.user)
        return render(request, "dashboard/channels-dashboard.html", {"subscribed": subscribed, "channels": channels, "user": request.user, "img": img})
    else:
        channels = Channel.objects.all()
        types = ChannelType.objects.all()
        return render(request, "index.html", {"channels": channels, "types": types})
    
def myprofile(request):
    if request.user.is_authenticated():
        subscribed = Subscription.objects.filter(user=request.user)
        channels = Channel.objects.filter(owner=request.user)
        img = getImage(request.user)
        return render(request, "dashboard/profile-dashboard.html", {"subscribed": subscribed, "channels": channels, "user": request.user, "img": img})
    else:
        channels = Channel.objects.all()
        types = ChannelType.objects.all()
        return render(request, "index.html", {"channels": channels, "types": types})
    
def mymessages(request):
    if request.user.is_authenticated():
        subscribed = Subscription.objects.filter(user=request.user)
        channels = Channel.objects.filter(owner=request.user)
        img = getImage(request.user)
        return render(request, "dashboard/messages-dashboard.html", {"subscribed": subscribed, "channels": channels, "user": request.user, "img": img})
    else:
        channels = Channel.objects.all()
        types = ChannelType.objects.all()
        return render(request, "index.html", {"channels": channels, "types": types})