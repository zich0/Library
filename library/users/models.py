from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserImage(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='image')
    image = models.ImageField(upload_to='user_images', null=True, blank=True)

