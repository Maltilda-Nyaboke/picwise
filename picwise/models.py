from uuid import uuid4
from django.db import models
from django import forms
import uuid
import datetime as dt
from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete
from django.utils.text import slugify
from django.urls import reverse
# from cloudinary.models import CloudinaryField

# Create your models here.

def user_directory_path(instance,filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Tag (models.Model):
    title = models.CharField(max_length=255,verbose_name='Tag')
    slug = models.SlugField(null=False,unique = True)

    class Meta:
        verbose_name_plural = 'Tags'
    def get_absolute_url(self):  
        return reverse('tags', args=(self.slug))  

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.slug)
            return super().save(*args, **kwargs)


class Image(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4(),editable=False)
    image = models.ImageField(upload_to=user_directory_path,verbose_name='image',null=True)
    name = models.CharField(max_length=35)
    caption = models.TextField()
    tags = models.ManyToManyField(Tag,related_name='tags')
    posted = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    likes= models.IntegerField(default=0)

    def get_absolute_url(self):  
        return reverse('imagedetails', args=[str(self.id)])

    def __str__(self):
        return self.name

    def save_image(self):
        self.save()

    def delete_image(self):
        self.delete()


class Profile(models.Model):
    profile_photo = models.ImageField(upload_to="media")
    username = models.CharField(max_length=20, null=True)
    bio = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.bio

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()


class Comment(models.Model):
    comment = models.TextField()

    def __str__(self):
        return self.comment

    def save_comment(self):
        self.save()

    def delete_comment(self):
        self.delete()


# class Likes(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.user

#     def save_like(self):
#         self.save()

#     def delete_like(self):
#         self.delete()

class Follow(models.Model):
    follower = models.ForeignKey(User,on_delete=models.CASCADE,related_name='follower',null=True)
    following = models.ForeignKey(User,on_delete=models.CASCADE,related_name='following',null=True)

    def __str__(self):
        return self.follower

    def save_follow(self):
        self.save()

    def delete_follow(self):
        self.delete()

class Stream(models.Model):
    following = models.ForeignKey(User,on_delete=models.CASCADE,related_name='stream_following')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE,null=True)
    date = models.DateTimeField()

    def add_image(sender,instance,*args,**kwargs):
        image = instance
        user = image.user
        followers = Follow.objects.all().filter(following=user)
        for follower in followers:
            stream= Stream(image=image,user=follower.follower,date=image.posted,following = user)
            stream.save()
  
    def __str__(self):
            return self.user

    def save_stream(self):
            self.save()

    def delete_stream(self):
            self.delete()

post_save.connect(Stream.add_image,sender= Image)            

    