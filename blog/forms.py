from django.forms import ModelForm, Textarea, SelectMultiple
from django.forms import PasswordInput, EmailInput, TextInput

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Post
from .models import Comment


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


class CreatePostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'category')
        widgets = {
            'title': TextInput(attrs={'class': 'form-control',
                                      'required': True,
                                      'placeholder': 'Type your title here..'
                                      }),
            'content': Textarea(attrs={'class': 'form-control',
                                       'required': True,
                                       'placeholder': 'Type your post here..'}),
            'category': SelectMultiple(attrs={'class': 'form-control',
                                              'required': True}),
        }


class CreateCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': TextInput(attrs={'class': 'form-control',
                                        'required': True,
                                        'placeholder': 'Your comment'})
        }
