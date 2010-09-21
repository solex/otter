from django import forms
from otter.main.models import *


class MessageForm(forms.Form):

    #TODO: Validation

    text = forms.CharField(widget=forms.Textarea)
    team_name = forms.CharField(required=False)
    user_name = forms.CharField(required=False)
    redirect = forms.CharField(required=False)

class FollowForm(forms.Form):

    #TODO: Validation

    team_name = forms.CharField(required=False)
    user_name = forms.CharField(required=False)
    follow = forms.BooleanField(required=False)
    redirect = forms.CharField(required=False)
