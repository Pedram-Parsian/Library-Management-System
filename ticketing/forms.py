from django import forms

from .models import Ticket, Reply


class TicketForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = Ticket
        fields = ['subject', 'priority', 'department']


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['text']
