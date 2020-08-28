from django.contrib.auth.forms import (
    AuthenticationForm
)
from django import forms
from ..users.models import User
from .models import Profile


class LoginForm(AuthenticationForm):
    """ログインフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label 


class UpdateProfile(forms.ModelForm):
    username = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    image = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ('username', 'email')

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user