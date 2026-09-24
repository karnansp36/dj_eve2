from django import forms
from .models import User_auth


class SignupForm(forms.ModelForm):
    class Meta:
        model = User_auth
        fields = "__all__"