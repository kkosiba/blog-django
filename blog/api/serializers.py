from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    RelatedField,
    DateTimeField,
    HiddenField,
    ValidationError,
)

from blog.models import Post, Category
from django.contrib.auth.models import User
from django.utils.text import slugify

from rest_framework.fields import CurrentUserDefault


# model listings
class CategoryListingField(RelatedField):
    def to_representation(self, value):
        return f"{value.name}"

    def to_internal_value(self, value):
        obj = Category.objects.filter(name=value)
        if obj and (len(obj)) == 1:
            return obj.get().id
        else:
            raise ValidationError("Category with name: %s does not exist" % value)


class AuthorListingField(RelatedField):
    def to_representation(self, value):
        return f"{value.username.capitalize()}"

    def to_internal_value(self, value):
        return value


# model serializers
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ("name",)


class PostListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name="post-detail", lookup_field="slug")
    author = AuthorListingField(queryset=User.objects.all())
    published_date = DateTimeField(format="%a, %d %b  %I:%M %p")

    class Meta:
        model = Post
        fields = ("url", "title", "published_date", "author")


class PostDetailSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name="post-detail", lookup_field="slug")
    author = AuthorListingField(queryset=User.objects.all())
    category = CategoryListingField(queryset=Category.objects.all(), many=True)
    published_date = DateTimeField(format="%a, %d %b  %I:%M %p")

    class Meta:
        model = Post
        fields = (
            "url",
            "title",
            "category",
            "content",
            "published_date",
            "author",
            "status",
        )


class PostCreateUpdateSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name="post-detail", lookup_field="slug")
    # author = AuthorListingField(queryset=User.objects.all())
    author = HiddenField(default=CurrentUserDefault())
    category = CategoryListingField(queryset=Category.objects.all(), many=True)
    published_date = DateTimeField(format="%a, %d %b  %I:%M %p", read_only=True)

    class Meta:
        model = Post
        fields = (
            "url",
            "title",
            "category",
            "content",
            "published_date",
            "author",
            "status",
        )

    def create(self, validated_data):
        title = validated_data.get("title", "")
        validated_data["slug"] = slugify(title)
        # pops out the list of categories
        categories = validated_data.pop("category")
        # and saves the rest of the data
        post = Post.objects.create(**validated_data)
        # add categories separately
        for category in categories:
            post.category.add(category)
        return post

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.slug = slugify(instance.title)

        categories = validated_data.get("category")
        # deassociate existing categories from instance
        instance.category.clear()
        for category in categories:
            instance.category.add(category)

        instance.author = self.context.get("request").user
        instance.content = validated_data.get("content", instance.content)
        instance.save()
        return instance
