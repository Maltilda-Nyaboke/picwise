from django.contrib.auth import login, authenticate
from .models import  Image, Profile
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class NewsLetterForm(forms.Form):
    your_name = forms.CharField(label='First Name',max_length=30)
    email = forms.EmailField(label='Email')

class EditProfileForm(ModelForm):
    class Meta():
        model=Profile
        fields=['profile_photo', 'bio', 'username']
        widgets = {
            'profile_photo': forms.FileInput(attrs={'class':'form-control mb-3'}),
            'bio': forms.TextInput(attrs={'class':'form-control mb-3'}),
            'username': forms.TextInput(attrs={'class':'form-control mb-3'}),
        }    