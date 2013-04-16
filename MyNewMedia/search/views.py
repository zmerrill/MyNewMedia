from channels.models import Channel
from django.shortcuts import render
from profiles.models import UserProfile
from django.db.models import Count
from django.db.models import Q

# Searches all channels for matches in either channels or users
def results(request):
    if 'q' in request.GET:
        # Uses string in URL to find query statement
        q = request.GET['q']
        message = q
        # Gets all channels where 'q' is contained in the title
        # the description, the type, or the owner
        channels = Channel.objects.filter(Q(title__icontains=q)
                                          | Q(description__icontains=q)
                                          | Q(type__type__icontains=q)
                                          | Q(owner__username__icontains=q)).annotate(num_sub=Count('subscription')).order_by('-num_sub')
        # Gets all artists where 'q' is found in the
        # username or biography
        artists = UserProfile.objects.filter(Q(owner__username__icontains=q) | Q(bio__icontains=q)).annotate(num_sub=Count('owner__channel')).order_by('-num_sub')
    else:
        message = 'You submitted an empty form.'
        channels = None
        artists = None
    
    # This information is used in the template be allowing the user to switch between viewing user results and channel results
    # as well as allowing them to filter the results down further
    return render(request, "search/channel-search.html", {"query": message, "channels": channels, "artists": artists})
