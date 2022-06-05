from django.contrib import admin
from .models import Image,Comment,Likes,Profile

# Register your models here.
admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(Likes)
admin.site.register(Profile)
