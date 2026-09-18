from django import forms
from .models import User_post


class User_postForm(forms.ModelForm):
    class Meta:
        model = User_post
        fields = ['title', 'description', 'image']