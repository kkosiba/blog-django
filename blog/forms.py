from django.forms import ModelForm, Textarea, SelectMultiple
from django.forms import PasswordInput, EmailInput, TextInput

from django.contrib.auth.models import User
from .models import Post
from .models import Comment


class CreateUserForm(ModelForm):
    password_confirm = PasswordInput(attrs={'class': 'form-control',
                                             'required': True,
                                             'placeholder': 'Confirm password'
                                             })
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {
            'username': TextInput(attrs={'class': 'form-control',
                                         'required': True,
                                         'placeholder': 'Username'
                                         }),
            'email': EmailInput(attrs={'class': 'form-control',
                                       'required': True,
                                       'placeholder': 'Email'
                                       }),
            'password': PasswordInput(attrs={'class': 'form-control',
                                             'required': True,
                                             'placeholder': 'Password'
                                             }),
        }


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
