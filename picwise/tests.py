from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from .models import Image, Profile, Like, Comment
from django.contrib.auth.models import User

# Create your tests here.
class ImageTestCase(TestCase):

    def setUp(self):
        """
        Create a image for testing
        """
        self.user=User(username='maltilda',email='maltildabosibori@gmail.com',password='Access')
        self.image=Image(image='food2.jpg',name='food',caption='sweetness',user=self.user)
        self.comment=Comment(image=self.image,user=self.user,content='what a meal!!')
        self.like=Like(image=self.image,user=self.user)
    def test_instance(self):
        self.assertTrue(isinstance(self.user,User))
        self.assertTrue(isinstance(self.image,Image))
        self.assertTrue(isinstance(self.comment,Comment))
        self.assertTrue(isinstance(self.like,Like))
    def test_save(self):
        self.user.save()
        self.image.save_image()
        self.comment.save_comments()
        self.like.save_likes()
        users = User.objects.all()
        images = Image.objects.all()
        comments = Comment.objects.all()
        likes = Like.objects.all()
        self.assertTrue(len(images) > 0)
        self.assertTrue(len(users) > 0)
        self.assertTrue(len(comments) > 0)
        self.assertTrue(len(likes) > 0)
    def test_update(self):
        self.user.save()
        self.image.save_image()
        self.image.update_caption('so pretty')
        caption_update=self.image.caption
        self.assertEqual(caption_update,'so pretty')

    def test_delete(self):
        self.user.save()
        self.image.save_image()
        self.comment.save_comments()
        self.like.save_likes()
        Like.objects.get(id =self.like.id).delete()
        Comment.objects.get(id =self.comment.id).delete()
        Image.objects.get(id =self.image.id).delete()
        User.objects.get(id =self.user.id).delete()
        likes=Like.objects.all()
        comments=Comment.objects.all()
        images=Image.objects.all()
        users=User.objects.all()
        self.assertTrue(len(images) == 0)
        self.assertTrue(len(users) == 0)
        self.assertTrue(len(comments) == 0)
        self.assertTrue(len(likes) == 0)