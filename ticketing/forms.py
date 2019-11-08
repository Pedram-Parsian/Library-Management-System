from django import forms
from django.conf import settings
from .validators import form_file_size_validator, file_type_validator, file_extension_validator

from .models import Ticket, Reply


class TicketForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea())
    attachments = forms.FileField(
        widget=forms.FileInput(
            attrs={'accept': ','.join(settings.VALID_ATTACHMENT_EXTENSIONS.keys()), 'multiple': True}), required=False,
        validators=(file_extension_validator, file_type_validator, form_file_size_validator))

    class Meta:
        model = Ticket
        fields = ['subject', 'priority', 'department']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean_attachments(self):
        if len(self.request.FILES.getlist('attachments')) > settings.MAX_ATTACHMENTS:
            self.add_error('attachments', 'Too many files!')
        return self.cleaned_data.get('attachments')


class ReplyForm(forms.ModelForm):
    attachments = forms.FileField(
        widget=forms.FileInput(
            attrs={'accept': ','.join(settings.VALID_ATTACHMENT_EXTENSIONS.keys()), 'multiple': True}), required=False,
        validators=(file_extension_validator, file_type_validator, form_file_size_validator))

    class Meta:
        model = Reply
        fields = ['text']
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean_attachments(self):
        if len(self.request.FILES.getlist('attachments')) > settings.MAX_ATTACHMENTS:
            self.add_error('attachments', 'Too many files!')
        return self.cleaned_data.get('attachments')
