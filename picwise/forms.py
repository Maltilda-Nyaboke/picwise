from django.contrib.auth import login, authenticate
from .models import  Image, Profile,Comment
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

# class LoginForm(UserCreationForm):

#     class Meta:
#         model = User
#         fields = ["username", "password"]


class NewsLetterForm(forms.Form):
    your_name = forms.CharField(label='First Name',max_length=30)
    email = forms.EmailField(label='Email')

class UpdateProfileForm(ModelForm):
    class Meta():
        model=Profile
        fields=['profile_photo', 'username','bio']
        exclude=['user']
        
class UploadImageForm(ModelForm):
    class Meta():
        model=Image
        fields=['image', 'name', 'caption']

class CommentForm(ModelForm):
    class Meta:
        model=Comment
        fields=['comment']        
        