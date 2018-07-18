from django.shortcuts import render, redirect
from django.utils import timezone

# for user management
from django.contrib.auth.models import User
# for post management
from .models import Post

from .forms import CreatePostForm
from .forms import CreateCommentForm

# for restricting access to adding post feature
from django.contrib.auth.decorators import login_required

# for user creation
from .forms import CreateUserForm

from django.contrib.auth import login

from django.shortcuts import get_object_or_404


def signup(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            # prepare data in cleaned form
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # save user to database
            user = User.objects.create_user(
                username=username, email=email, password=password)

            # login user after signup
            login(request, user)
            # and redirect to the main page
            return redirect('/')
    else:
        form = CreateUserForm()

    return render(request, 'blog/signup.html', {'form': form})


# adding posts feature
@login_required
def add(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CreatePostForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            author = User.objects.get_by_natural_key(request.user.username)
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            published_date = timezone.now()
            # post_tags = form.cleaned_data['tags']

            Post.objects.create(author=author, title=title,
                                content=content, published_date=published_date)
            # redirect to main page
            # todo: redirect to just added post
            return redirect('/')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = CreatePostForm()

    return render(request, 'blog/add.html', {'form': form})


# adding comments feature
@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            # get currently logged user
            author = User.objects.get_by_natural_key(request.user.username)
            content = form.cleaned_data['content']
            post.comments.objects.create(author=author, content=content)
            return redirect('/')
    else:
        form = CreateCommentForm()

    return render(request, 'blog/add_comment.html', {'form': form})


def index(request):
    list_of_posts = Post.objects.order_by('-published_date')
    context = {
        'list_of_posts': list_of_posts
    }
    return render(request, 'blog/posts.html', context)


def about(request):
    return render(request, 'blog/about.html', {})


def contact(request):
    return render(request, 'blog/contact.html', {})
