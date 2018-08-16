from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Post, Category

from .forms import (
    AddPostForm, ContactForm, SignUpForm)

# complex lookups (for searching)
from django.db.models import Q

from django.urls import reverse_lazy

# class based views
from django.views.generic.edit import (
    CreateView, DeleteView,
    UpdateView, FormView)

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView

from django.views.generic.dates import (
    YearArchiveView, MonthArchiveView, DayArchiveView)

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.contrib.auth.decorators import login_required
from django.db import transaction

class SignUp(CreateView):
    template_name = 'registration/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')

    # prevents signed in user to sign up
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(*args, **kwargs)


class ListPosts(ListView):
    model = Post
    context_object_name = 'list_posts'
    template_name = 'blog/list_posts.html'
    paginate_by = 10
    ordering = ('-published_date',)


class ListAuthors(ListView):
    model = Post
    template_name = 'blog/list_posts_author.html'
    paginate_by = 10
    ordering = ('-published_date',)


class ListByAuthor(ListView):
    pass


class ListTags(ListView):
    pass


class ListByTag(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/list_by_tag.html'
    paginate_by = 10
    ordering = ('-published_date',)

    def get_queryset(self):
        tag = self.kwargs.get('tag_name', None)
        results = []
        if tag:
            results = Post.objects.filter(
                tags__name=tag)
        return results


class ListCategories(ListView):
    model = Category
    template_name = 'blog/list_categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ListByCategory(ListView):
    template_name = 'blog/post_archive_category.html'

    def get_queryset(self):
        self.category = get_object_or_404(Category,
            category=self.kwargs['category'])
        return Post.objects.filter(category__name=self.category.name)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the category
        context['category'] = self.category.name
        return context


class DetailsPost(DetailView):
    model = Post
    template_name = 'blog/details_post.html'


# Post archive views
class PostYearArchive(YearArchiveView):
    queryset = Post.objects.all()
    date_field = "published_date"
    make_object_list = True
    allow_future = True


class PostYearMonthArchive(MonthArchiveView):
    queryset = Post.objects.all()
    date_field = "published_date"
    allow_future = True


class PostYearMonthDayArchive(DayArchiveView):
    queryset = Post.objects.all()
    date_field = "published_date"
    allow_future = True


# Create, delete and update post views
class AddPost(LoginRequiredMixin, CreateView):
    model = Post
    form_class = AddPostForm

    # to process request.user in the form
    def form_valid(self, form):
        form.save(commit=False)
        form.instance.author = self.request.user
        return super().form_valid(form)


# not yet implemented
class PostDraftsList(LoginRequiredMixin, ListView):
    template_name = 'blog/list_drafts.html'

    def get_queryset(self):
        self.category = get_object_or_404(Category,
            category=self.kwargs['category'])
        return Post.objects.filter(status='DRAFT',
                                   author__email=self.request.username)


class DeletePost(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')

    def test_func(self):
        """
        Only let the user delete object if they own the object being deleted
        """
        return self.get_object().author.first_name == self.request.user.first_name


class UpdatePost(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = AddPostForm

    def test_func(self):
        """
        Only let the user update object if they own the object being updated

        """
        return self.get_object().author.first_name == self.request.user.first_name


class SearchPosts(ListView):
    model = Post
    context_object_name = 'list_posts'
    template_name = 'blog/search_posts.html'
    paginate_by = 10
    ordering = ('-published_date',)

    def get_queryset(self):
        search_query = self.request.GET.get('q', None)
        results = []
        if search_query:
            results = Post.objects.filter(
                Q(category__name__icontains=search_query) |
                Q(author__email__icontains=search_query) |
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query)).distinct()
        return results


class About(TemplateView):
    template_name = 'blog/about.html'


class Contact(FormView):
    template_name = 'blog/contact.html'
    form_class = ContactForm
    success_url = 'success/'

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })