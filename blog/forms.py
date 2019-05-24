from django import forms

from django.forms import (
    ModelForm,
    Textarea,
    TextInput,
    EmailField,
    EmailInput,
    SelectMultiple,
    CharField,
    PasswordInput,
    ClearableFileInput,
    Select,
    CheckboxInput,
)

from django.utils.text import slugify
from django.utils.crypto import get_random_string

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Category, Post

from django.core.exceptions import ValidationError


# class UserForm(ModelForm):
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'email', )


# class ProfileForm(ModelForm):
#     class Meta:
#         model = Profile
#         fields = ('avatar', 'bio', )


# class SignUpForm(UserCreationForm):
#     username = CharField(label='Username',
#         widget=TextInput(
#             attrs={'class': 'form-control',
#                    'required': True,
#                    }))
#     email = EmailField(label='Email',
#         widget=EmailInput(
#             attrs={'class': 'form-control',
#                    'required': True,
#                    }))
#     password1 = CharField(label='Password',
#         widget=PasswordInput(
#             attrs={'class': 'form-control',
#                    'required': True,
#                    }))
#     password2 = CharField(label='Confirm password',
#         widget=PasswordInput(
#             attrs={'class': 'form-control',
#                    'required': True,
#                    }))

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2', )

#     def clean_username(self):
#         username = self.cleaned_data.get('username')
#         qs = User.objects.filter(username=username)
#         if qs.exists():
#             raise ValidationError("Username already in use!")
#         return username

#     def save(self, commit=True):
#         instance = super().save(commit=False)
#         instance.first_name = self.cleaned_data.get('username', '').capitalize()
#         instance.email = self.cleaned_data.get('email', '')
#         if commit:
#             instance.save()
#         return instance


def make_slug(instance, new_slug=None):
    """
    Function for creating unique slugs
    """

    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    # check if there exists a post with existing slug
    q = Post.objects.filter(slug=slug)
    if q.exists():
        new_slug = "-".join([slug, get_random_string(4, "0123456789")])
        return make_slug(instance, new_slug=new_slug)
    return slug


class AddPostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ("slug", "author")
        widgets = {
            "title": TextInput(
                attrs={
                    "required": True,
                    "placeholder": "Type your title here...",
                    "class": "form-control",
                }
            ),
            "category": SelectMultiple(
                attrs={"required": True, "class": "form-control"}
            ),
            "status": Select(attrs={"required": True, "class": "form-control"}),
            "allow_comments": CheckboxInput(
                attrs={"required": True, "class": "form-control"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        slug = cleaned_data.get("slug")

        if not slug and title:
            cleaned_data["slug"] = slugify(title)

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.slug = make_slug(instance)

        if commit:
            instance.save()
            self.save_m2m()
        return instance
