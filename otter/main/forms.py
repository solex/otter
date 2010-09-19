from django import forms
from otter.main.models import *

#class MessageForm(forms.ModelForm):
#
#    class Meta:
#        model = Message
#        exclude = ('sender',)

class MessageForm(forms.Form):

    #TODO: Validation

    text = forms.CharField()
    team_name = forms.CharField(required=False)
    user_name = forms.CharField(required=False)
    redirect = forms.CharField(required=False)


