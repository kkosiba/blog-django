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
from django.views.generic.base import TemplateView

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
    paginate_by = 10
    ordering = ('-published_date',)


class ListPostsByAuthor(ListView):
    pass


class ListPostsByYearView(ListView):
    model = Post
    template_name = 'blog/post_actions/list_posts_year.html'
    paginate_by = 10
    ordering = ('-published_date',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(
            published_date__year=self.kwargs.get('year', None))
        return context


class ListPostsByYearMonthView(ListView):
    model = Post
    template_name = 'blog/post_actions/list_posts_year_month.html'
    paginate_by = 10
    ordering = ('-published_date',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(
            published_date__month=self.kwargs.get('month', None))
        return context


class ListCategoriesView(ListView):
    model = Category
    template_name = 'blog/post_actions/list_categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ListPostsByCategoryView(ListView):
    template_name = 'blog/post_actions/list_posts_category.html'

    def get_queryset(self):
        self.category = get_object_or_404(Category,
            category=self.kwargs['category'])
        return Post.objects.filter(category__name=self.category)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the category
        context['category'] = self.category.name
        return context


class DetailsPostView(DetailView):
    model = Post
    template_name = 'blog/post_actions/single_post.html'


# def index(request, category=None, year=None, month=None, slug=None):
#     list_of_posts = Post.objects.all()

#     if category is not None:
#         list_of_posts = list_of_posts.filter(category__name__icontains=category)
#     if year is not None:
#         list_of_posts = list_of_posts.filter(published_date__year=year)
#     if month is not None:
#         list_of_posts = list_of_posts.filter(published_date__month=month)
#     if slug is not None:
#         list_of_posts = list_of_posts.filter(category__name__contains=category)

#     template = 'blog/post_actions/list_posts.html'
#     context = {
#         'list_of_posts': list_of_posts,
#     }
#     return render(request, template, context)


# def year(request, year):
#     return index(request, year=year)


# def year_month(request, year, month):
#     return index(request, year=year, month=month)


# def category(request, name):
#     return index(request=request, category=name)


class AddPostView(CreateView):
    model = Post
    form_class = AddPostForm

    def get_form_kwargs(self):
        """
        Override to get currently authenticated user as post author
        """
        kwargs = super(AddPostView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class DeletePostView(DeleteView):
    model = Post
    success_url = reverse_lazy('index')


class UpdatePostView(UpdateView):
    model = Post
    form_class = AddPostForm


class SearchPostsView(ListView):
    model = Post
    context_object_name = 'list_posts'
    template_name = 'blog/post_actions/search_posts.html'
    paginate_by = 10
    ordering = ('-published_date',)

    def get_queryset(self):
        search_query = self.request.GET.get('q', None)
        results = []
        if search_query:
            results = Post.objects.filter(
                Q(category__name__icontains=search_query) |
                Q(author__username__icontains=search_query) |
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query)).distinct()
        return results


def about(request):
    return render(request, 'blog/about.html', {})


def contact(request):
    return render(request, 'blog/contact.html', {})
