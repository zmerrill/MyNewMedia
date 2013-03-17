#from PIL import Image as PImage
from django.shortcuts import render
from os.path import join as pjoin
from profiles.forms import ProfileForm
from profiles.models import UserProfile
from MyNewMedia.settings import MEDIA_ROOT

def profile(request, pk):
    """Edit user profile."""
    profile = UserProfile.objects.get(user=pk)
    img = None

    if request.method == "POST":
        pf = ProfileForm(request.POST, request.FILES, instance=profile)
        if pf.is_valid():
            pf.save()
            # resize and save image under same filename
            imfn = pjoin(MEDIA_ROOT, profile.avatar.name)
            #im = PImage.open(imfn)
            #im.thumbnail((160,160), PImage.ANTIALIAS)
            #im.save(imfn, "JPEG")
    else:
        pf = ProfileForm(instance=profile)

    if profile.avatar:
        img = "/media/" + profile.avatar.name
    return render(request, "dashboard/user-home.html", {"pf": pf, "img": img})
        
