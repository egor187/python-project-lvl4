from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['first_name'].required = True
    #     self.fields['last_name'].required = True

    class Meta(UserCreationForm):
        model = CustomUser
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username',)