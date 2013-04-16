from channels.models import Channel, Link
from subscriptions.models import Subscription
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


# Adds a subscription under the logged in user for the passed extension
def subscribe(request, ext):
    user = request.user
    channel = Channel.objects.get(url_ext=str(ext))
    links = Link.objects.filter(channel=channel).count()
    # Creates subscription here - save is implicit in the create() call
    Subscription.objects.create(user=user, channel=channel, unread=links)
    return HttpResponseRedirect(reverse("channels.views.channelhome", args=[ext]))

# Removes a subscription if it exists
def unsubscribe(request, ext):
    user = request.user
    channel = Channel.objects.get(url_ext=str(ext))
    Subscription.objects.get(user=user, channel=channel).delete()
    return HttpResponseRedirect(reverse("channels.views.channelhome", args=[ext]))


