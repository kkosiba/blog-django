from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

# for user management
from django.contrib.auth.models import User
# for post management
from .models import Post
# for Categories
from .models import Category

from .forms import AddPostForm
from .forms import CreateCommentForm

# for restricting access to adding post feature
from django.contrib.auth.decorators import login_required

# for user creation
from .forms import CreateUserForm

from django.contrib.auth import authenticate, login, logout

# for signup exception handling
from django.core.exceptions import ValidationError

# complex lookups (for searching)
from django.db.models import Q

from django.urls import reverse_lazy

# class based views
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView


# register new user
def signup(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            # prepare data in cleaned form
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)

            # if User.objects.filter(username=username).count() > 1:
            #     raise ValidationError('Username already in use!')
            # if User.objects.filter(email=email).count() > 1:
            #     raise ValidationError('Email already exists!')
            # if password != password_confirm:
            #     raise ValidationError('Passwords do not match!')

            # login user after signup
            login(request, user)
            # and redirect to the main page
            return redirect('signup_successful.html')  # doesn't work... yet
    else:
        form = CreateUserForm()

    return render(request, 'blog/signup.html', {'form': form})


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

    return render(request, 'blog/posts.html', {'form': form})


class ListPostsView(ListView):
    model = Post
    context_object_name = 'list_posts'
    template_name = 'blog/post_actions/list_posts.html'
    paginate_by = 3
    ordering = ('-published_date',)


class ListPostsByYearView(ListView):
    model = Post
    context_object_name = 'list_posts'
    template_name = 'blog/post_actions/list_posts.html'
    paginate_by = 3
    ordering = ('-published_date',)

    def get_context_data(self, *args, **kwargs):
        """
        Filter by year if it is provided in GET parameters
        """
        context = super(ListPostsByYearView, self).get_context_data(*args, **kwargs)
        context['year'] = 2018
        return context

class ListPostsByYearMonthView(ListPostsByYearView):
    def get_queryset(self):
        """
        Filter by year and month if it is provided in GET parameters
        """
        queryset = super().get_queryset(self)
        if 'month' in self.request.GET:
            queryset = queryset.filter(
                published_date__month=self.request.GET['month'])


class ListPostsByCategoryView(ListView):
    pass


class DetailsPostView(DetailView):
    model = Post
    template_name = 'blog/post_actions/single_post.html'


def index(request, category=None, year=None, month=None, slug=None):
    list_of_posts = Post.objects.all()

    if category is not None:
        list_of_posts = list_of_posts.filter(category__name__icontains=category)
    if year is not None:
        list_of_posts = list_of_posts.filter(published_date__year=year)
    if month is not None:
        list_of_posts = list_of_posts.filter(published_date__month=month)
    if slug is not None:
        list_of_posts = list_of_posts.filter(category__name__contains=category)

    template = 'blog/post_actions/list_posts.html'
    context = {
        'list_of_posts': list_of_posts,
    }
    return render(request, template, context)


def year(request, year):
    return index(request, year=year)


def year_month(request, year, month):
    return index(request, year=year, month=month)


def category(request, name):
    return index(request=request, category=name)


class AddPostView(CreateView):
    model = Post
    form_class = AddPostForm


class DeletePostView(DeleteView):
    model = Post
    success_url = reverse_lazy('index')


class UpdatePostView(UpdateView):
    model = Post
    form_class = AddPostForm


# def add_post(request):
#     """
#     View for adding new posts (only for authenticated users)
#     """

#     # create a form instance and populate it with data from the request
#     # if a GET (or any other method), create a blank form
#     form = CreatePostForm(request.POST or None)
#     # check whether it's valid:
#     if form.is_valid():
#         form.save()
#         form = CreatePostForm() # rerender the form

#     template = 'blog/post_actions/add.html'
#     context = {
#         'form': form,
#     }
#     return render(request, template, context)



# def delete_post(request, slug):
#     """
#     View for deleting posts by slug
#     """
#     post = get_object_or_404(Post, slug=slug)
#     if request.method == 'POST':
#         post.delete()
#         redirect('/')

#     template = 'blog/post_actions/delete.html'
#     context = {
#         'form': form,
#     }
#     return render(request, template, context)


@login_required
def update_post(request, slug):
    """
    View for deleting posts by slug
    """
    # todo

    template = 'blog/post_actions/update.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


def search(request):
    list_of_posts = Post.objects.all()
    page = 'blog/posts.html'

    search = request.GET.get('search')
    if search:
        list_of_posts = list_of_posts.filter(
            Q(category__name__icontains=search) |
            Q(author__username__icontains=search) |
            Q(title__icontains=search) |
            Q(content__icontains=search)
        ).distinct()
    else:
        return render(request, page, {})

    context = {
        'list_of_posts': list_of_posts,
    }
    return render(request, page, context)


def about(request):
    return render(request, 'blog/about.html', {})


def contact(request):
    return render(request, 'blog/contact.html', {})
