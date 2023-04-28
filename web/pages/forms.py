from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

from .models import Item

class PostItem(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["title", "description", "price", "image", "deadline_at", "category"]

class Settings(UserChangeForm):
    password = None
    username = None

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )
