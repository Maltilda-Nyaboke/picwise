from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import login,authenticate,logout
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from django.template import loader
from .forms import NewsLetterForm,UpdateProfileForm,UploadImageForm,CommentForm
from django.http import HttpResponse, Http404,HttpResponseRedirect
from .email import send_welcome_email
from picwise.models import *

# Create your views here.
@login_required(login_url='login')
def home(request):
    images = Image.objects.all()
    profile = Profile.objects.all()
    return render(request,'index.html',{'images':images,'profile':profile})
def all_comments(request, image_id):
    image = Image.objects.get(id=image_id)
    comments = Comment.objects.filter(image=image)

    return render(request,'index.html',{'comments':comments})
def profile(request):
    user = request.user.pk
    profile = User.objects.all()
    profile_image = Profile.objects.filter(user=request.user.pk)
    following_count = Follow.objects.filter(follower=user).count()
    followers_count = Follow.objects.filter(following=user).count()
    images = Image.objects.all()
    context = {'profile': profile, 'images': images, 'following_count':following_count,'followers_count':followers_count,}
    return render(request,'profile.html',context)    

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
        # form =  LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        # Redirect to a success page.
            return redirect(request,'index.html')
        else:
            return redirect(request,'registration/login.html')

# Return an 'invalid login' error message.
    else: 
        # form = LoginForm()
        return render(request,'registration/login.html') 
def logout_user(request):
    logout(request)
    return redirect('login')         

def search_results(request):
    query = request.GET.get('query')
    if query:
        profiles = Profile.search_profile(query)

        
        params = {'profiles': profiles,'query': query}
    
        return render(request, 'search.html',params)


@login_required
def add_comment(request,image_id):
    image = get_object_or_404(Image, id=image_id)
    comments = Comment.objects.filter(image=image).order_by('posted')
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
    return render(request, 'comment.html', { 'form':form, 'image_id':image_id,'comments':comments})
    

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
@login_required
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

def like_image(request, image_id):
    user = request.user
    image=Image.objects.get(id=image_id)
    current_likes=image.likes
    liked=Like.objects.filter(user=user,image=image).count()
    if not liked:
        like=Like.objects.create(user=user,image=image)
        current_likes=current_likes + 1

    else:
        Like.objects.filter(user=user,image=image).delete()
        current_likes= current_likes- 1
    image.likes=current_likes
    image.save()
    return HttpResponseRedirect(reverse('home'))
            
def follow(request, pk):
    if request.method == 'GET':
        try:
            user_profile = User.objects.get(username=pk)
        except User.DoesNotExist:
            user_profile = None

        follow_s = Follow(follower=request.user, following=user_profile)
        follow_s.save()
        return redirect('profile')

def unfollow(request, pk):
    if request.method == 'GET':
        try:
            user_profile = User.objects.get(username=pk)
        except User.DoesNotExist:
            user_profile = None

        unfollow_d = Follow.objects.filter(follower=request.user, following=user_profile)
        unfollow_d.delete()
        return redirect('profile')        