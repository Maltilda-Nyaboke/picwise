from django.db import models

# Create your models here.
class Image(models.Model):
    image = 
    name = models.CharField(max_length=30)
    caption = models. TextField()
    user = models.ForeignKey


    def __str__(self):
        return self.name

    def save_image(self):
        self.save()    
    def delete_image(self):
        self.delete()