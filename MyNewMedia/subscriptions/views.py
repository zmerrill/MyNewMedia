from channels.models import Channel, Link
from subscriptions.models import Subscription
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

def subscribe(request, ext):
    user = request.user
    channel = Channel.objects.get(url_ext=str(ext))
    links = Link.objects.filter(channel=channel).count()
    Subscription.objects.create(user=user, channel=channel, unread=links)
    return HttpResponseRedirect(reverse("channels.views.channelhome", args=[ext]))

def unsubscribe(request, ext):
    user = request.user
    channel = Channel.objects.get(url_ext=str(ext))
    Subscription.objects.get(user=user, channel=channel).delete()
    return HttpResponseRedirect(reverse("channels.views.channelhome", args=[ext]))


