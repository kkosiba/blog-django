from django.forms import ModelForm, Select, Textarea, DateTimeInput
from django.forms import PasswordInput, EmailInput, TextInput

from django.contrib.auth.models import User
from .models import Post


class CreateUserForm(ModelForm):
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
                                             })
        }


class CreatePostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('author', 'title', 'content', 'published_date')
        widgets = {
            'author': Select(attrs={'class': 'form-control',
                                    'required': True}),
            'title': TextInput(attrs={'class': 'form-control',
                                      'required': True,
                                      'placeholder': 'Post title'
                                      }),
            'content': Textarea(attrs={'class': 'form-control',
                                       'required': True,
                                       'placeholder': 'Contents'}),
            'published_date': DateTimeInput()  # this needs to be improved...
        }


# class CreateCommentForm(ModelForm):
#     class Meta:
#         model = Comment
#         fields = ('author', 'content')
