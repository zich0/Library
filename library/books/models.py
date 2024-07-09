from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    cover_image = models.ImageField(upload_to='author_covers', null=True, blank=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True, related_name='books')
    year_published = models.IntegerField()
    description = models.TextField()
    cover_image = models.ImageField(upload_to='book_covers', null=True, blank=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

