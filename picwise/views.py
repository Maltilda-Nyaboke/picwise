from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from django.template import loader
from .forms import NewsLetterForm,EditProfileForm
from django.http import HttpResponse, Http404,HttpResponseRedirect
from .emails import send_welcome_email
from picwise.models import Image,NewsLetterRecipients,Profile,Follow

# Create your views here.
#@login_required
def home(request):
    posts = Image.objects.all()
    return render(request,'index.html',{'posts':posts})
def profile(request,id):
    
    return render(request,'profile.html')    

def register(request):
    if request.method == 'POST':
        form =  RegisterForm(request.POST)

        if form.is_valid():
            form.save()
        return redirect(request,'index.html')
    else:    
        form = RegisterForm()
    return render(request,'register.html',{'form':form}) 

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        # Redirect to a success page.
            return redirect(request,'index.html')
        else:
            return redirect(request,'login.html')

# Return an 'invalid login' error message.
    else: 
        return render(request,'login.html')  

def update_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    form = EditProfileForm(request.POST, instance=profile)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('profile')
    context = {'form': form}
    return render(request, 'update.html', context)

def search_results(request):
  if 'name' in request.GET and request.GET["name"]:
    name = request.GET.get('name')
    users = Profile.search_profiles(name)
    images = Image.search_images(name)
    print(users)
    return render(request, 'search.html', {"users": users, "images": images})
  else:
    return render(request, 'search.html')
def news_today(request):
    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['your_name']
            email = form.cleaned_data['email']

            recipient = NewsLetterRecipients(name = name,email =email)
            recipient.save()
            send_welcome_email(name,email)

            HttpResponseRedirect('news_today')
        else:
            form = NewsLetterForm()
    return render(request, 'all-news/today-news.html', {"letterForm":form})        

