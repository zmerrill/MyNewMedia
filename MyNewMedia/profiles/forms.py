from django.forms import ModelForm
from profiles.models import UserProfile, UserPreferences

class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ["page_views", "owner"]
        
class PreferencesForm(ModelForm):
    class Meta:
        model = UserPreferences
        exclude = ["profile"]
