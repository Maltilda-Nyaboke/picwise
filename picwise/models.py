from django.db import models
from django import forms
import datetime as dt
from django.contrib.auth.models import User

# from cloudinary.models import CloudinaryField


# Create your models here.
class Image(models.Model):
    name = models.CharField(max_length=30)
    caption = models. TextField()
    user = models.ForeignKey


    def __str__(self):
        return self.name

    def save_image(self):
        self.save()    
    def delete_image(self):
        self.delete()


class Profile(models.Model):
    profile_photo=models.ImageField(upload_to = 'media')
    bio=models.TextField()
    username=models.CharField(max_length=20,null=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)   

class Comment(models.Model):
    comment = models.TextField()    
