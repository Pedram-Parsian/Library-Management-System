from django import forms
from .models import Ticket


class TicketForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = Ticket
        fields = ['subject', 'priority', 'department']
