from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from django.template import loader
from .forms import NewsLetterForm,UpdateProfileForm,UploadImageForm,CommentForm
from django.http import HttpResponse, Http404,HttpResponseRedirect
from .emails import send_welcome_email
from picwise.models import Image,NewsLetterRecipients,Profile,Follow,Comment

# Create your views here.
#@login_required
def home(request):
    images = Image.objects.all()
    return render(request,'index.html',{'images':images})
def profile(request):
    user = request.user
    profile = Profile.objects.all()
    following_count = Follow.objects.filter(follower=user).count()
    followers_count = Follow.objects.filter(following=user).count()
    images = Image.objects.all()
    context = {'profile': profile, 'images': images, 'following_count':following_count,'followers_count':followers_count,}

    

    return render(request,'profile.html',context)    

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

def search_results(request):
  if 'name' in request.GET and request.GET["name"]:
    name = request.GET.get('name')
    users = Profile.search_profiles(name)
    images = Image.search_images(name)
    print(users)
    return render(request, 'search.html', {"users": users, "images": images})
  else:
    return render(request, 'search.html')
def add_comment(request,image_id):
    images=Image.objects.get(id=image_id)
    comments=Comment.objects.filter(images=images).all()
    current_user=request.user
    if request.method =='POST':
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = current_user
            
            comment.image = images
            comment.save()
        return redirect('home')
    else:
        
        form = CommentForm()
    return render(request, 'index.html', {'images': images, 'form':form, 'comments':comments})
    

def profile_update(request,id):
    profile = Profile.objects.get(id=id)
    form = UpdateProfileForm(request.POST, instance=profile)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('profile')
    context = {'form': form}
    return render(request, 'profile_update.html',context) 

def upload_image(request):
    form = UploadImageForm()
    user = request.user
    owner = Profile.objects.get(user=user)
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
    return render(request, 'gram_app/upload.html', context)
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

