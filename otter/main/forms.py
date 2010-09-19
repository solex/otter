from django import forms
from otter.main.models import *

class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        exclude = ('sender',)

