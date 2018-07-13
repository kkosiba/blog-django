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

    # # comments
    # comments = models.ForeignKey(Comment, on_delete=models.CASCADE)

    # title
    title = models.CharField(max_length=300)

    # post content
    content = models.TextField()

    # tags
    # tags = models.ManyToManyField(Tag)

    # date of publication
    published_date = models.DateTimeField(blank=True, null=True)

    # string representation returning title of a post
    def __str__(self):
        return self.title


# class Tag(models.Model):
#     """
#     Django database model for tag system
#     """
#     # tag name
#     tag_name = models.CharField(max_length=20)
#
#     def __str__(self):
#         return self.tag_name


class Comment(models.Model):
    """
    Django database model for comment feature
    """

    # author of a comment
    author = models.CharField(max_length=70)

    # associate comment with a post
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')

    # comment's content (no longer than 500 symbols)
    content = models.TextField(max_length=500)

    # date of comment creation
    created = models.DateTimeField(default=timezone.now)

    # approved?
    approved = models.BooleanField(default=False)

    # approve comment
    def approve(self):
        self.approved = True
        self.save()

    # string representation returning comment's content
    def __str__(self):
        return self.content
