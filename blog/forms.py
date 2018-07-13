from django.forms import ModelForm, Select, TextInput, Textarea, DateTimeInput
from .models import Post, Comment


class PostForm(ModelForm):
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


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'content')
