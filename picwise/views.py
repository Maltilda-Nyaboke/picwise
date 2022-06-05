from django.shortcuts import render
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def home(request):
    return render(request,'index.html')

def register(request):
    return render(request,'register.html')    