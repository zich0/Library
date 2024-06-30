from django.db import models
from django.contrib.auth.models import User
from books.models import Book


# Create your models here.
class UserImage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_image')
    image = models.ImageField(upload_to='user_images', null=True, blank=True)


class Favorite(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True, related_name='favorite')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite')
    added_at = models.DateTimeField(auto_now_add=True)

