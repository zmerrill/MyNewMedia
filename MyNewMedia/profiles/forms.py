from django.forms import ModelForm
from profiles.models import UserProfile, UserPreferences

# User profile edit form
class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ["page_views", "owner"]
    
# User preference edit form
class PreferencesForm(ModelForm):
    class Meta:
        model = UserPreferences
        exclude = ["profile"]
