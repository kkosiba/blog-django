from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

# class Profile(models.Model):
#     user = models.OneToOneField(User,
#     	on_delete=models.CASCADE,
#         default=User,
#         null=True,
#         related_name='profile', )
#     avatar = models.ImageField(
#         upload_to='media/avatars',
#         default='media/avatars/none.jpg',
#         blank=True, )
#     bio = models.TextField(max_length=500, default='', blank=True)


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
