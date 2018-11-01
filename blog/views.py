from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Post, Category
from taggit.models import Tag

from .forms import (
    AddPostForm, ContactForm, SignUpForm,
    UserForm, ProfileForm, )

# complex lookups (for searching)
from django.db.models import Q

from django.urls import reverse_lazy

# class based views
from django.views.generic.edit import (
    CreateView, DeleteView, UpdateView, FormView)

from django.views import View
from django.utils.decorators import method_decorator

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView

from django.views.generic.dates import (
    YearArchiveView, MonthArchiveView, DayArchiveView)

from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin)

from django.db import transaction


class CategoryDatesMixin(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        # get queryset of datetime objects for all published posts
        context['dates'] = Post.objects.filter(
            status='PUBLISHED').datetimes(field_name='published_date',
                                          kind='month',
                                          order='DESC')
        context['recent_posts'] = Post.objects.filter(
                                        status='PUBLISHED') \
                                    .order_by('-published_date')[:3]
        return context


class SignUp(CategoryDatesMixin, CreateView):
    template_name = 'registration/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')

    # prevents signed in user to sign up
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(*args, **kwargs)


class ListPosts(CategoryDatesMixin, ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    ordering = ('-published_date',)
    paginate_by = 10


class ListByAuthor(CategoryDatesMixin, ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/posts_by_author.html'
    paginate_by = 10
    ordering = ('-published_date',)

    def get_queryset(self):
        author = self.kwargs.get('author', None)
        results = []
        if author:
            results = Post.objects.filter(
                author__first_name=author)
        return results

    def get_context_data(self, **kwargs):
        """
        Pass author's name to the context
        """
        context = super().get_context_data(**kwargs)
        context['author'] = self.kwargs.get('author', None)
        return context


class ListByTag(CategoryDatesMixin, ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/posts_by_tag.html'
    paginate_by = 10
    ordering = ('-published_date',)

    def get_queryset(self):
        tag = self.kwargs.get('tag', None)
        results = []
        if tag:
            results = Post.objects.filter(
                tags__name=tag)
        return results

    def get_context_data(self, **kwargs):
        """
        Pass tag name to the context
        """
        context = super().get_context_data(**kwargs)
        context['tag'] = self.kwargs.get('tag', None)
        return context

class ListByCategory(CategoryDatesMixin, ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/posts_by_category.html'
    paginate_by = 10
    ordering = ('-published_date',)

    def get_queryset(self):
        category = self.kwargs.get('name', None)
        results = []
        if category:
            results = Post.objects.filter(
                category__name=category)
        return results

    def get_context_data(self, **kwargs):
        """
        Pass category's name to the context
        """
        context = super().get_context_data(**kwargs)
        context['category'] = self.kwargs.get('name', None)
        return context


class DetailsPost(CategoryDatesMixin, DetailView):
    model = Post
    template_name = 'blog/details_post.html'


# Post archive views
class ArchiveMixin(object):
    model = Post
    date_field = "published_date"
    allow_future = False
    context_object_name = 'posts'


class PostYearArchive(CategoryDatesMixin, ArchiveMixin, YearArchiveView):
    make_object_list = True


class PostYearMonthArchive(CategoryDatesMixin, ArchiveMixin, MonthArchiveView):
    pass


# Create, delete and update post views
class AddPost(CategoryDatesMixin,
              PermissionRequiredMixin,
              LoginRequiredMixin,
              CreateView):
    form_class = AddPostForm
    permission_required = 'blog.add_post'
    template_name = 'blog/post_form.html'

    # to process request.user in the form
    def form_valid(self, form):
        form.save(commit=False)
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDraftsList(CategoryDatesMixin,
                     PermissionRequiredMixin,
                     LoginRequiredMixin,
                     ListView):
    template_name = 'blog/list_drafts.html'
    permission_required = 'blog.add_post'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(
            status='DRAFT',
            author__first_name=self.request.user.first_name)


class DeletePost(CategoryDatesMixin,
                 LoginRequiredMixin,
                 UserPassesTestMixin,
                 DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')

    def test_func(self):
        """
        Only let the user delete object if they own the object being deleted
        """
        return self.get_object().author.first_name == self.request.user.first_name


class UpdatePost(CategoryDatesMixin,
                 LoginRequiredMixin,
                 UserPassesTestMixin, 
                 UpdateView):
    model = Post
    form_class = AddPostForm

    def test_func(self):
        """
        Only let the user update object if they own the object being updated

        """
        return self.get_object().author.first_name == self.request.user.first_name


class SearchPosts(CategoryDatesMixin, ListView):
    context_object_name = 'posts'
    template_name = 'blog/search_posts.html'
    paginate_by = 10
    ordering = ('-published_date',)

    def get_queryset(self):
        search_query = self.request.GET.get('q', None)
        results = []
        if search_query:
            results = Post.objects.filter(
                Q(category__name__icontains=search_query) |
                Q(author__first_name__icontains=search_query) |
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query)).distinct()
        return results


class Contact(CategoryDatesMixin, FormView):
    template_name = 'blog/contact.html'
    form_class = ContactForm
    success_url = 'success/'

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


class UpdateProfile(LoginRequiredMixin, View):
    """
    Update user and profile simult.
    Cannot pass additional context fields through CategoryDatesMixin,
    since View has no get_context_data() attr.
    """
    def get(self, request, *args, **kwargs):
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        return render(request, 'profiles/profile.html', {
            'user_form': user_form,
            'profile_form': profile_form,
            'categories': Category.objects.all(),
            'dates': Post.objects.filter(
            status='PUBLISHED').datetimes(field_name='published_date',
                                          kind='month',
                                          order='DESC')
            })

    @method_decorator(transaction.atomic)
    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
        return render(request, 'profiles/profile.html', {
            'user_form': user_form,
            'profile_form': profile_form,
            'categories': Category.objects.all(),
            'dates': Post.objects.filter(
            status='PUBLISHED').datetimes(field_name='published_date',
                                          kind='month',
                                          order='DESC')
            })
