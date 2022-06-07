from django.contrib import admin
from .models import Image, Comment,Profile,Follow,Like,NewsLetterRecipients

# Register your models here.
admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Follow)
admin.site.register(Like)
admin.site.register(NewsLetterRecipients)
