from django.forms import ModelForm
from channels.models import Channel, Link

# Form used to add new channels
# used in channel dashboard page
class ChannelForm(ModelForm):
    class Meta:
        model=Channel
        
# Form used to add new links to a channel
# used in the channel home page
class LinkForm(ModelForm):
    class Meta:
        model=Link
        