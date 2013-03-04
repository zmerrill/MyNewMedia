from channels.models import Channel, Link
from channels.forms import ChannelForm, LinkForm
from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

def home(request, ext):
    channel = Channel.objects.get(url_ext=str(ext))
    links = Link.objects.filter(channel=channel)
    d = dict(channel=channel, links=links, user=request.user, form=LinkForm())
    d.update(csrf(request))
    return render_to_response("channel/channel-home.html", d)

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
    return HttpResponseRedirect(reverse("channels.views.home", args=[ext]))