from django.db import models

class User(models.Model):
    username = models.CharField(max_length = 64)
    password = models.CharField(max_length = 200)
    date_joined = models.DateTimeField('Member Since')
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    birthday = models.DateTimeField('Birthday')
    location = models.CharField(max_length = 200)
    biography = models.CharField(max_length = 1000)
    avatar_path = models.CharField(max_length = 256)

class Channel(models.Model):
    channel_name = models.CharField(max_length = 200)
    user_owner = models.ForiegnKey(User)
    description = models.CharField(max_length = 1000)
    channel_type = models.ForiegnKey(Channel_Types)
    image_path = models.CharField(max_length = 256)
    date_added = models.DateTimeField('Date Added')

class Subscription(models.Model):
    channel = models.ForiegnKey(Channel)
    user = models.ForiegnKey(User)
    date_added = models.DateTimeField('Date Added')

class Channel_Types(models.Model):
    channel_type = models.CharField(max_length = 64)
    date_added = models.DateTimeField('Date Added')

class Link(models.Model):
    channel = models.ForiegnKey(Channel)
    link_type = models.ForiegnKey(Link_Types)
    link_url = models.CharField(max_length = 10000)

class Link_Types(models.Model):

class Tags(models.Model):

class Link_Tags(models.Model):
