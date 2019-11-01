from django import forms
from bootstrap_modal_forms.forms import BSModalForm
from .models import Ticket


class TicketCreateForm(BSModalForm):
    text = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = Ticket
        fields = ['subject', 'priority', 'department']
