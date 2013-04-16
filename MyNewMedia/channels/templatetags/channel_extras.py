import feedparser #feedparser.org
import datetime
from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def subtract(first, second):
    return first - second

@register.inclusion_tag('template_extensions/feed.html')
def pull_feed(feed_url, posts_to_show=5):
    feed = feedparser.parse(feed_url)
    posts = []
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
            'image': img
            })
        
        
    return {'posts': posts}

register.inclusion_tag('template_extensions/feed.html')(pull_feed)
