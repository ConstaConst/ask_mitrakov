from django import forms
from django.core.exceptions import ValidationError

from questions.models import *


class RegForm(forms.Form):
    username = forms.CharField(max_length=16, required=True)
    nickname = forms.CharField(max_length=16, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, required=True)

    avatar = forms.ImageField()

    def clean_password(self):
        value = self.cleaned_data['password']
        if len(value) < 8:
            raise forms.ValidationError('Password is too short')
        return value

    def save(self):
        return Profile.objects.create(
            user=User.objects.create_user(
                username=self.cleaned_data['username'],
                password=self.cleaned_data['password']
            ),
            nickname=self.cleaned_data['nickname'],
            avatar=self.cleaned_data['avatar']
        )


class SettingForm(forms.Form):
    username = forms.CharField(max_length=16)
    nickname = forms.CharField(max_length=16)

    avatar = forms.ImageField()

    def change_user(self, user):
        username=self.cleaned_data['username']
        nickname = self.cleaned_data['nickname']
        avatar=self.cleaned_data['avatar']
        if username:
            user.username = username
        if nickname:
            user.profile.nickname = nickname
        if avatar:
            user.profile.avatar = avatar
        return user
