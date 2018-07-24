from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Post(models.Model):
    CHOICES = (
        ('draft', 'Draft'),
        ('submitted', 'Submitted'), )

    class Meta:
        ordering = ('-published_date', )

    # posts' category (many-to-many)
    category = models.ManyToManyField(Category, blank=False)

    # author (many Posts to one User)
    # only Users can be post authors
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique_for_date='published_date')
    content = models.TextField()

    published_date = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=CHOICES, default='draft')

    def __str__(self):
        return self.title


class Comment(models.Model):
    CHOICES = (
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'), )

    # bind comment to author and post
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    content = models.TextField(max_length=500)

    created_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=CHOICES, default='rejected')

    def __str__(self):
        return self.content
