from django.shortcuts import render
from channels.models import Channel, ChannelType

def index(request):
    channels = Channel.objects.all()
    types = ChannelType.objects.all()
    return render(request, "index.html", {"channels": channels, "types": types})