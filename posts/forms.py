from django import forms
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError
from .models import Category, Post


def make_slug(instance, new_slug=None):
    """Function for creating unique slugs"""

    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    # check if there exists a post with existing slug
    q = Post.objects.filter(slug=slug)
    if q.exists():
        new_slug = "-".join([slug, get_random_string(4, "0123456789")])
        return make_slug(instance, new_slug=new_slug)
    return slug


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ("slug", "author")
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "required": True,
                    "placeholder": "Type your title here...",
                    "class": "form-control",
                }
            ),
            "category": forms.SelectMultiple(
                attrs={"required": True, "class": "form-control"}
            ),
            "status": forms.Select(attrs={"required": True, "class": "form-control"}),
            "allow_comments": forms.CheckboxInput(
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
