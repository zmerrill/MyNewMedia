from django.shortcuts import render
from channels.models import Channel, ChannelType
from subscriptions.models import Subscription

def index(request):
    if request.user.is_authenticated():
        subscribed = Subscription.objects.filter(user=request.user)
        channels = Channel.objects.filter(owner=request.user)
        return render(request, "dashboard/user-home.html", {"subscribed": subscribed, "channels": channels, "user": request.user})
    else:
        channels = Channel.objects.all()
        types = ChannelType.objects.all()
        return render(request, "index.html", {"channels": channels, "types": types})