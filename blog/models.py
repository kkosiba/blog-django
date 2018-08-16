from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils import timezone
from django.urls import reverse

# tags
from taggit.managers import TaggableManager

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, 
        default=None, null=True, related_name='profile')
    avatar = models.ImageField(
        upload_to='media/avatars',
        default='media/avatars/none.jpg',
        blank=True, )
    bio = models.TextField(max_length=500, default='', blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'name': self.name})


class Post(models.Model):
    STATUS = (
        ('DRAFT', 'Draft'),
        ('PUBLISHED', 'Published'),
    )

    category = models.ManyToManyField(Category, blank=False)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts')
    picture = models.ImageField(upload_to='media', default='media/None/no-img.jpg')
    title = models.CharField(max_length=300)
    slug = models.SlugField(
        max_length=300,
        unique_for_date='published_date')
    content = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
    allow_comments = models.BooleanField(default=True)
    status = models.CharField(default='DRAFT', choices=STATUS, max_length=10)

    # tags mechanism
    tags = TaggableManager()

    class Meta:
        ordering = ('-published_date', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:details_post', kwargs={'slug': self.slug})