from django.shortcuts import render
from channels.models import Channel, ChannelType, FeedItem, FeedTracker
from subscriptions.models import Subscription
from profiles.models import UserProfile
from recommendations.views import loadRecommendations

# Finds image from dynamic media folder
def getImage(user):
    try:
        profile = UserProfile.objects.get(owner=user)
        if(profile.avatar):
            img = "/media/" + profile.avatar.name
        else:
            img = None
    except UserProfile.DoesNotExist:
        profile = None
        img = None
    return img

# Main index view for the site
# will redirect to the splash page if the user is nto logged in
# otherwise it will redirect to the subscription
# manager of the dashboard specific to the logged in user
def index(request):
    # Check for logged in user
    if request.user.is_authenticated():
        # Get logged in user's list of subscriptions, channels, recommendations, history and profile
        subscribed = Subscription.objects.filter(user=request.user)
        channels = Channel.objects.filter(owner=request.user)
        itemcounts = {}
        items = {}
        read = {}
        readcounts = {}
        unreadcounts = {}
        img = getImage(request.user)
        # References the recommendation app
        recs = loadRecommendations(request)
        # the value_list filter returns only a specific column in a model list
        # in this case we want only the 'channel' column in order to query the
        # FeedItem and FeedTracker tables so we can get the user's history
        for c in subscribed.values_list('channel', flat=True):
            items[c] = FeedItem.objects.filter(channel=c)
            read[c] = FeedTracker.objects.filter(user=request.user, channel=c).values_list('item', flat=True)
            itemcounts[c] = FeedItem.objects.filter(channel=c).count()
            readcounts[c] = FeedTracker.objects.filter(user=request.user, channel=c).count()
            unreadcounts[c] = itemcounts[c] - readcounts[c]
        # Return all of this information to the user-home dashboard page
        return render(request, "dashboard/user-home.html", {"subscribed": subscribed, "channels": channels, "user": request.user, "img": img, "recs": recs, "counts": itemcounts, "items": items, "read": read, "readcounts": readcounts, "unreadcounts": unreadcounts})
    else: # If the user is not logged in redirect to the splash page
        channels = Channel.objects.all()
        types = ChannelType.objects.all()
        return render(request, "index.html", {"channels": channels, "types": types})

# redirects to the channel manager section of the dashboard. returns most
# of the same information as the subscription page above
def mychannels(request):
    if request.user.is_authenticated():
        subscribed = Subscription.objects.filter(user=request.user)
        channels = Channel.objects.filter(owner=request.user)
        img = getImage(request.user)
        itemcounts = {}
        for c in channels:
            itemcounts[c.id] = FeedItem.objects.filter(channel=c).count()
        return render(request, "dashboard/channels-dashboard.html", {"subscribed": subscribed, "channels": channels, "user": request.user, "img": img, "counts": itemcounts})
    else:
        channels = Channel.objects.all()
        types = ChannelType.objects.all()
        return render(request, "index.html", {"channels": channels, "types": types})

# not used currently
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
    
# redirects to the messaging section of the dashboard. please refer to 
# https://code.google.com/p/django-messages/
# for documentation
def mymessages(request):
    if request.user.is_authenticated():
        subscribed = Subscription.objects.filter(user=request.user)
        channels = Channel.objects.filter(owner=request.user)
        img = getImage(request.user)
        return render(request, "messages/inbox.html", {"subscribed": subscribed, "channels": channels, "user": request.user, "img": img})
    else:
        channels = Channel.objects.all()
        types = ChannelType.objects.all()
        return render(request, "index.html", {"channels": channels, "types": types})