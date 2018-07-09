from django.db import models
from django.utils import timezone

# Create your models here.


class Post(models.Model):
    """
    Django database model for posts
    """

    # author
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    # title
    title = models.CharField(max_length=300)
    # post content
    content = models.TextField()
    # date of creation
    created = models.DateTimeField(default=timezone.now)
    # date of publication
    published = models.DateTimeField(blank=True, null=True)

    # method for publishing posts
    def submit(self):
        self.published = timezone.now()
        self.save()

    # string representation returning title of a post
    def __str__(self):
        return self.title
