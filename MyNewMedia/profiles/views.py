from PIL import Image as PImage 
from django.shortcuts import render
from os.path import join as pjoin
from profiles.forms import ProfileForm
from profiles.models import UserProfile
from MyNewMedia.settings import MEDIA_ROOT

# redirects to the profile editor section of the dashboard. the user can edit profile information here
def profile(request):
    """Edit user profile."""
    try:
        profile = UserProfile.objects.get(owner=request.user)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(owner=request.user)
    img = None
    
    # Submit profile information and save changes
    if request.method == "POST":
        pf = ProfileForm(request.POST, request.FILES, instance=profile)
        if pf.is_valid():
            pf.save()
            #resize and save image under same filename
            imfn = pjoin(MEDIA_ROOT, profile.avatar.name)
            im = PImage.open(imfn)
            im.thumbnail((200,200), PImage.ANTIALIAS)
            im.save(imfn, "JPEG")
    else:
        # Create new instance of profile form
        pf = ProfileForm(instance=profile)

    # Find the avatar picture if it exists
    if profile.avatar:
        img = "/media/" + profile.avatar.name
    return render(request, "dashboard/profile-dashboard.html", {"pf": pf, "img": img, "profile": profile})
        
