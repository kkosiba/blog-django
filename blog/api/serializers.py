from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    )

from blog.models import Post, Category
from django.contrib.auth.models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', )


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', )


class PostSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='post-detail',
        lookup_field='slug',
        )
    author = UserSerializer()
    category = CategorySerializer(many=True)

    class Meta:
        model = Post
        fields = (
            'url',
            'author',
            'category',
            'content',
            'published_date',
            )
