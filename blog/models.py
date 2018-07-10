from django.db import models
# from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Author(models.Model):
    """
    Django database model for post's author
    """
    # author's name (assuming names <=70 symbols)
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    Django database model for posts
    """

    # author (many Posts to one Author)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    # title
    title = models.CharField(max_length=300)
    # post content
    content = models.TextField()
    # date of creation
    created = models.DateTimeField(blank=True, null=True)

    # method for publishing posts
    def submit(self):
        self.created = timezone.now()
        self.save()

    # string representation returning title of a post
    def __str__(self):
        return self.title


#
# class Comment(models.Model):
#     """
#     Django database model for comment feature
#     """
#
#     # comment's author
#     com_author = models.ForeignKey(User)
#
#     # comment's content (no longer than 500 symbols)
#     com_content = models.TextField(max_length=500)
#
#     # submit a comment
#     def com_submit(self):
#         self.save()
#
#     # string representation returning comment's contenttypes
#     def __str__(self):
#         return self.com_content
