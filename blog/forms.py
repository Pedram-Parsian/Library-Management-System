from django.conf import settings
from django import forms


class LogedInUser_CommentForm(forms.Form):
    text = forms.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)


class AnonymousUser_CommentForm(forms.Form):
    name = forms.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)
    email = forms.EmailField()
    text = forms.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)
