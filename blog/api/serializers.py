from rest_framework.serializers import ModelSerializer

from blog.models import Post
from django.contrib.auth.models import User


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'id',
            'category',
            'author',
            'slug',
            'content',
            'published_date',
            )


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', )
