from django.forms import ModelForm
from channels.models import Channel, Link

class ChannelForm(ModelForm):
    class Meta:
        model=Channel
        
class LinkForm(ModelForm):
    class Meta:
        model=Link
        