from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import login,authenticate,logout
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from django.template import loader
from .forms import NewsLetterForm,UpdateProfileForm,UploadImageForm,CommentForm
from django.http import HttpResponse, Http404,HttpResponseRedirect
from .email import send_welcome_email
from picwise.models import *

# Create your views here.
@login_required
def home(request):
    images = Image.objects.all()
    return render(request,'index.html',{'images':images})
def profile(request):
    user = request.user
    profile = User.objects.all()
    profile_image = Profile.objects.filter(user=request.user.pk)
    # following_count = Follow.objects.filter(follower=user).count()
    # followers_count = Follow.objects.filter(following=user).count()
    # images = Image.objects.all()
    # context = {'profile': profile, 'images': images, 'following_count':following_count,'followers_count':followers_count,}
    return render(request,'profile.html',{'profile':profile,'user':user})    

def register(request):
    if request.method == 'POST':
        form =  RegisterForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['username']
            email = form.cleaned_data['email']

            recipient = NewsLetterRecipients(name = name,email =email)
            recipient.save()
            send_welcome_email(name,email)
            form.save()
            return HttpResponseRedirect(reverse('home'))
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

def search_results(request):
  if 'name' in request.GET and request.GET["name"]:
    name = request.GET.get('name')
    users = Profile.search_profiles(name)
    images = Image.search_images(name)
    print(users)
    return render(request, 'search.html', {"users": users, "images": images})
  else:
    return render(request, 'search.html')

@login_required
def add_comment(request,image_id):
    user = request.user
    if request.method == 'POST':
        image = Image.objects.filter(id = image_id).first()
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment= form.save(commit=False)
            comment.user = user.profile
            comment.image = image
            comment.save()
            return redirect('home')
    else:
        
        form = CommentForm()
    return render(request, 'comment.html', { 'form':form, 'image_id':image_id})
    

def profile_update(request):
    form = UpdateProfileForm()
    user = request.user.id
    profile = Profile.objects.get(user_id=user)
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile.profile_photo = form.cleaned_data.get('profile_photo')
            profile.username = form.cleaned_data.get('username')
            profile.bio = form.cleaned_data.get('bio')
            profile.save()

            return redirect('profile')
        else:
            form= UpdateProfileForm()
    return render(request, 'profile_update.html',{'form':form}) 

def upload_image(request):
    form = UploadImageForm()
    user = request.user
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            name = form.cleaned_data['name']
            caption = form.cleaned_data['caption']
            upload = Image(image=image, name=name,
                           caption=caption, user=user)
            upload.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'upload.html', context)
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
def like_image(request, image_id):
    user = request.user
    image=Image.objects.get(id=image_id)
    current_likes=image.likes
    print(type(current_likes),'current_likes')
    liked=Like.objects.filter(user=user,image=image).count()
    if not liked:
        liked=Like.objects.create(user=user,image=image)
        current_likes=current_likes+1

    else:
        liked=Like.objects.filter(user=user,image=image).delete()
        current_likes=current_likes- 1
    image.likes=current_likes
    image.save()
    print(image)
    return HttpResponseRedirect(reverse('home'))
    # image = get_object_or_404(Image,id = image_id)
    # like = Like.objects.filter(image = image ,user = request.user).first()
    # if like is None:
    #     like = Like()
    #     like.image = image
    #     like.user = request.user
    #     like.save()
    # else:
    #     like.delete()
    return redirect('home')         

