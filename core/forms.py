from django import forms
from django.core.mail import send_mail
from django.conf import settings


class ContactForm(forms.Form):
    name = forms.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)
    email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)
    message = forms.CharField(max_length=settings.TEXTFIELD_MAX_LENGTH, widget=forms.Textarea)

    def send_mail(self):
        subject = f'Contact us form - from {self.cleaned_data["name"]}'
        message = f"From: {self.cleaned_data['name']}\nEmail: {self.cleaned_data['email']}\nSubject:" \
                  f" {self.cleaned_data['subject']}\nMessage: {self.cleaned_data['message']}"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = ['pedram_parsian@outlook.com']
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
