from channels.models import Channel, Link, ChannelType
from PIL import Image as PImage
from os.path import join as pjoin
from MyNewMedia.settings import MEDIA_ROOT
from django.contrib.auth.models import User
from subscriptions.models import Subscription
from channels.forms import ChannelForm, LinkForm
from channels.models import FeedItem, FeedTracker
from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, RequestContext
from django.core.urlresolvers import reverse
from profiles.models import UserProfile
import datetime
import feedparser #feedparser.org
from django.http import HttpResponseRedirect

# Channel home page view
# Displays all content and information about a channel.
def channelhome(request, ext):
    # Get channel, feed items, and manual links from the passed URL extension
    channel = Channel.objects.get(url_ext=str(ext))
    items = FeedItem.objects.filter(channel=channel)
    links = Link.objects.filter(channel=channel).order_by('-created')
    # Check for logged in user
    # if logged in then check for subscription
    if(request.user.is_authenticated()):
        try:
            # Get subscription
            subscription = Subscription.objects.get(user=request.user, channel=channel)
        except Subscription.DoesNotExist:
            # None if not subscribed
            subscription = None
        
    else:
        # If not logged in then indicate - this is checked in the template
        subscription = "NotLoggedIn"
        
    # Get a count of subscriptions for the channel
    try:
        count = Subscription.objects.filter(channel=channel)
    except Subscription.DoesNotExist:
        count = None
    
    # Use the pull_feed function to pull in all RSS items from the channel.feed URL
    # There is a limit of 1000 total feed items pulled back
    posts = pull_feed(channel.feed, 1000) 
    
    # Save pulled feed items into the appropriate tables if they 
    # don't already exist
    for p in posts:
        try:
            items.get(title=p['title'])
        except FeedItem.DoesNotExist:
            new = FeedItem.objects.create(title=p['title'], channel=channel, link=p['link'], itemcount=p['id'])
            new.save()
    
    # Add all items to the dictionary
    d = dict(channel=channel, links=links, user=request.user, form=LinkForm(), subscription=subscription, count=count, posts=posts)
    d.update(csrf(request))
    # Render the template with the dictionary
    return render_to_response("channel/channel-home.html", d, context_instance=RequestContext(request))

# Adds the passed feed item to a user's history
# This returns a response only by default
# Its called with AJAX so nothing will ever be
# rendered
def MarkAsRead(request, pTitle, c):
    channel = Channel.objects.get(title=c)
    post = FeedItem.objects.get(itemcount=pTitle, channel=channel)
    user = request.user
    try:
        item = FeedTracker.objects.get(user=user, item=post, channel=post.channel)
    except FeedTracker.DoesNotExist:
        item = FeedTracker.objects.create(user=user, item=post, channel=post.channel)
    d = dict(item=item)
    return render_to_response("template_extensions/loader.html", d)
    

# Uses the feedparser package to pull an RSS feed XML for use
# refer to
# https://code.google.com/p/feedparser/
# for more information
def pull_feed(feed_url, posts_to_show=5):
    feed = feedparser.parse(feed_url)
    posts = []
    
    # Shrink the passed post limit to avoid out of bounds exception
    if len(feed['entries']) < posts_to_show:
        posts_to_show = len(feed['entries'])
    
    # For each returned RSS feed item
    # -Find the published dates
    # -Get all media - audio, video, images - if they exist
    # Add the feed item to the posts list
    for i in range(posts_to_show):
        pub_date = feed['entries'][i].updated_parsed
        published = datetime.date(pub_date[0], pub_date[1], pub_date[2] )
        audio = None
        video = None
        links = feed['entries'][i].links
        try: 
            img = feed.feed.image.href
        except AttributeError:
            img = None
            
        for l in links:
            if l.type.find('audio') != -1:
                audio = l['href']
            elif l.type.find('video') != -1:
                video = l['href']
                
        
        posts.append({
            'title': feed['entries'][i].title,
            #'subtitle': feed['entries'][i].subtitle,
            'summary': feed['entries'][i].summary,
            'link': feed['entries'][i].link,
            'audio': audio,
            'video': video,
            'date': published,
            'image': img,
            'id': i
            })
        
    # Return the list of posts
    return posts

# Create a dictionary organized by type for use in the browse page
# Not much logic needed since the user will filter based on their needs
def browsechannels(request):
    channels = Channel.objects.all()
    types = ChannelType.objects.all()
    d = {}
    for ctype in types:
        d[ctype.type] = channels.filter(type=ctype)
        
    return render_to_response("search/channel-browse.html", {"d": d, "user": request.user})   

# Currently not used. Eventually will allow the feed to be polled for updates
def ajaxFeedPull(request, ext):
    channel = Channel.objects.get(url_ext=str(ext))
    d = dict(channel=channel)
    return render_to_response("template_extensions/loader.html", d)

# Returns information about the artist as well
# as all channels that belong to that artist
def artisthome(request, ext):
    artist = User.objects.get(username=str(ext))
    try:
        # Load artist profile and avatar
        profile = UserProfile.objects.get(owner=artist)
        if(profile.avatar):
            img = "/media/" + profile.avatar.name
        else:
            img = None
    except UserProfile.DoesNotExist:
        img = None
        profile = None
    # Get all channels created by artist
    channels = Channel.objects.filter(owner=artist).order_by('-created')
    d = dict(artist=artist, channels=channels, user=request.user, form=ChannelForm(), img=img, profile=profile)
    return render(request, "channel/artist-home.html", d)

# Adds a channel - note that this is used in the dashboard page, not the channels page.
def add(request):
    # If the form has been submitted then validate the data contains no errors
    # if there are no errors then create the new channel and pull the feed from the given URL
    if request.method == 'POST':
        form = ChannelForm(request.POST, request.FILES)
        if form.is_valid():
                channel = form.save()
                imfn = pjoin(MEDIA_ROOT, channel.image.name)
                im = PImage.open(imfn)
                im.thumbnail((200,200), PImage.ANTIALIAS)
                im.save(imfn, "JPEG")
                posts = pull_feed(channel.feed, 1000) 
                for p in posts:
                    new = FeedItem.objects.create(title=p['title'], channel=channel, link=p['link'], itemcount=p['id'])
                    new.save()
        # Return the user to the channels dashboard
        return redirect("/channels/")
    # If the form was not submitted, then render the form for use        
    else:
        form = ChannelForm(initial={'owner': request.user})
        try:
            profile = UserProfile.objects.get(owner=request.user)
            if(profile.avatar):
                img = "/media/" + profile.avatar.name
            else:
                img = None
        except UserProfile.DoesNotExist:
            img = None
        
        return render(request, "dashboard/add-channel.html", {"form": form, "img": img})
    
# Allows a user to edit an existing channel
def edit(request, pk):
    # Show the user's profile
    try:
        profile = UserProfile.objects.get(owner=request.user)
        if(profile.avatar):
            img = "/media/" + profile.avatar.name
        else:
            img = None
    except UserProfile.DoesNotExist:
        img = None
        
    # Get the current channel information
    try:
        channel=Channel.objects.get(pk=pk)
    except Channel.DoesNotExist:
        return redirect("/channels/")  
    
    # Redirect if the current user is not the owner
    if(request.user != channel.owner):
        return redirect("/channels/")
    
    # If the form was submitted then check for errors and save the changes
    if request.method == "POST":
        cf = Channel(request.POST, instance=channel)
        if cf.is_valid():
            cf.save()
    # Otherwise create a new instance of the form
    else:
        cf = ChannelForm(instance=channel)
    return render(request, "dashboard/channel-edit.html", {"cf": cf, "channel": channel, "owner": channel.owner, "img": img})
    
    
# Adds a new link to the channel - used on the channel home page
def addlink(request,ext):
    p=request.POST
    # Saves the new link if the form contains no errors.
    if p.has_key("title") and p["title"] and p.has_key("url") and p["url"]:
            link = Link(channel=Channel.objects.get(url_ext=str(ext)))
            lf = LinkForm(p, initial={'channel': Channel.objects.get(url_ext=str(ext))})
            link = lf.save()
            link.channel = Channel.objects.get(url_ext=str(ext))
            link.save()
    # Redirects back to the channel home page
    return HttpResponseRedirect(reverse("channels.views.channelhome", args=[ext]))

# Allows owner to delete a channel.
# Takes the primary key that identifies a channel
def deletechannel(request,pk):
    Channel.objects.get(pk=pk).delete()
    return HttpResponseRedirect(reverse("core.views.index"))
