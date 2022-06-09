from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete


# Create your models here.

class Image(models.Model):
    image = models.ImageField(upload_to='media',null=True)
    name = models.CharField(max_length=35)
    caption = models.TextField()
    posted = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    likes= models.IntegerField(default=0)


    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-posted']

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='post_like')

    def user_liked_post(sender, instance, *args, **kwargs):
            like = instance
            post = like.post
            sender = like.user

    def user_unlike_post(sender, instance, *args, **kwargs):
            like = instance
            post = like.post
            sender = like.user


class NewsLetterRecipients(models.Model):
    name = models.CharField(max_length = 30)
    email = models.EmailField()   


class Profile(models.Model):
    profile_photo = models.ImageField(upload_to='media')
    username = models.CharField(max_length=20, null=True)
    bio = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    
    def __str__(self):
        return self.bio

    def save_profile(self):
        self.save()    
    @classmethod
    def search_profile(cls, query):
            profs = cls.objects.filter(user__username__icontains=query)
            return profs


    

class Comment(models.Model):
    comment = models.TextField()
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    posted = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
            return self.comment
class Follow(models.Model):
    follower = models.ForeignKey(User,on_delete=models.CASCADE,related_name='follower',null=True)
    following = models.ForeignKey(User,on_delete=models.CASCADE,related_name='following',null=True)
    def user_follow(sender, instance, *args, **kwargs):
        follow = instance
        sender = follow.follower
        following = follow.following

    def user_unfollow(sender, instance, *args, **kwargs):
        follow = instance
        sender = follow.follower
        following = follow.following

    