from django.forms import ModelForm, Textarea, SelectMultiple
from django.forms import PasswordInput, EmailInput, TextInput

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Post
from .models import Comment

from django.utils.text import slugify


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)
        # widgets = {
        #     'username': TextInput(attrs={'class': 'form-control',
        #                                  'required': True,
        #                                  'placeholder': 'Username'
        #                                  }),
        #     'email': EmailInput(attrs={'class': 'form-control',
        #                                'required': True,
        #                                'placeholder': 'Email'
        #                                }),
        #     'password1': PasswordInput(attrs={'class': 'form-control',
        #                                       'required': True,
        #                                       'placeholder': 'Password'
        #                                       }),
        #     'password2': PasswordInput(attrs={'class': 'form-control',
        #                                       'required': True,
        #                                       'placeholder': 'Confirm password'
        #                                       }),
        # }


class AddPostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ('slug',)
        widgets = {
            'title': TextInput(
                attrs={
                    'class': 'form-control',
                    'required': True,
                    'placeholder': 'Type your title here..', }, ),
            'content': Textarea(
                attrs={
                    'class': 'form-control',
                    'required': True,
                    'placeholder': 'Type your post here..', }, ),
            'category': SelectMultiple(
                attrs={
                    'class': 'form-control',
                    'required': True, }, ),
        }

    def clean(self):
        cleaned_data = super(AddPostForm, self).clean()
        title = cleaned_data.get('title')
        slug = cleaned_data.get('slug')

        if not slug and title:
            cleaned_data['slug'] = slugify(title)

        return cleaned_data

    def save(self, commit=True):
        instance = super(AddPostForm, self).save(commit=False)
        instance.slug = slugify(self.cleaned_data.get('title', ''))

        if commit:
            instance.save()
            self.save_m2m()
        return instance


class CreateCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': TextInput(attrs={'class': 'form-control',
                                        'required': True,
                                        'placeholder': 'Your comment'})
        }
