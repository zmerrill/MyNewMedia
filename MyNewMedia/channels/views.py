from channels.models import Channel, Link
from django.contrib.auth.models import User
from subscriptions.models import Subscription
from channels.forms import ChannelForm, LinkForm
from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


def channelhome(request, ext):
    channel = Channel.objects.get(url_ext=str(ext))
    links = Link.objects.filter(channel=channel).order_by('-created')
    if(request.user.is_authenticated()):
        try:
            subscription = Subscription.objects.get(user=request.user, channel=channel)
        except Subscription.DoesNotExist:
            subscription = None
    else:
        subscription = "NotLoggedIn"
    d = dict(channel=channel, links=links, user=request.user, form=LinkForm(), subscription=subscription)
    d.update(csrf(request))
    return render_to_response("channel/channel-home.html", d)

def artisthome(request, ext):
    artist = User.objects.get(username=str(ext))
    channels = Channel.objects.filter(owner=artist).order_by('-created')
    d = dict(artist=artist, channels=channels, user=request.user, form=ChannelForm())
    return render(request, "channel/artist-home.html", d)

def add(request):
    if request.method == 'POST':
        form = ChannelForm(request.POST)
        if form.is_valid():
                form.save()
        return redirect("/../index")        
    else:
        form = ChannelForm(initial={'owner': request.user})
        return render(request, "channel/add-channel.html", {"form": form})
    
def addlink(request,ext):
    p=request.POST
    
    if p.has_key("title") and p["title"] and p.has_key("url") and p["url"]:
            link = Link(channel=Channel.objects.get(url_ext=str(ext)))
            lf = LinkForm(p, initial={'channel': Channel.objects.get(url_ext=str(ext))})
            link = lf.save()
            link.channel = Channel.objects.get(url_ext=str(ext))
            link.save()
    return HttpResponseRedirect(reverse("channels.views.channelhome", args=[ext]))

def deletechannel(request,pk):
    Channel.objects.get(pk=pk).delete()
    return HttpResponseRedirect(reverse("core.views.index"))

