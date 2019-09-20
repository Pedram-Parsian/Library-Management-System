from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField, UserChangeForm
from django.contrib.auth import authenticate
from django.urls import reverse
from django.utils.safestring import mark_safe
from captcha.fields import ReCaptchaField
from . import models


class CustomUserCreationForm(UserCreationForm):
    captcha = ReCaptchaField()

    class Meta:
        model = models.User
        fields = ("email", "first_name", "last_name", 'captcha')
        field_classes = {"email": UsernameField}


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(strip=False, widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        if email is not None and password:
            self.user = authenticate(self.request, email=email, password=password)
            if self.user is None:
                raise forms.ValidationError("Invalid email/password combination.")
            if self.user.email_activated:
                # successful login
                pass
            else:
                resend_activation_email_url = reverse('resend_activation_email')
                message = f'Your email has not been confirmed! Please confirm your email or ' \
                          f'<a href="{resend_activation_email_url}">Request a new one.</a>'
                raise forms.ValidationError(mark_safe(message))
        return self.cleaned_data

    def get_user(self):
        return self.user


class ReactivateEmailForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = models.EmailActivation.objects.email_exists(email)
        if not qs.exists():
            signup_link = reverse('signup')
            message = f"This email does not exists, would you like to <a href='{signup_link}'>Sign up</a>?"
            raise forms.ValidationError(mark_safe(message))
        # if only one of the user's EmailActivation (either time_expired or not) has FORCED_EXPIRED, we shouldn't allow
        # the user to resend a activation email.
        if models.EmailActivation.objects.email_exists(email).filter(forced_expired=True).exists():
            contact_link = reverse('contact')
            message = f"Your email activation has been expired explicitly by our admins, So you can not resend" \
                      f" activation email! <a href='{contact_link}'>Contact the admins</a> to fix it."
            raise forms.ValidationError(mark_safe(message))
        return email


class UpdateInfo(UserChangeForm):
    def __init__(self, instance, *args, **kwargs):
        super(UpdateInfo, self).__init__(*args, **kwargs)
        self.instance = instance

    class Meta:
        model = models.User
        fields = ('first_name', 'last_name')
