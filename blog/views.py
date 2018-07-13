from django.shortcuts import render, redirect
from django.utils import timezone

from .models import Post, Comment
from .forms import PostForm, CommentForm

# Create your views here.


def years_archive(request, year):
    # posts = Post.objects.filter(created__year=year)
    # comments = Post.comments
    # context = {
    #     'year': year,
    #     'posts': posts,
    #     'comments': comments
    # }
    # return render(request, 'blog/years_archive.html', context)
    pass


def month_archive(request, year, month):
    # lst = Post.objects.filter(created__year=year, created__month=month)
    # context = {
    #     'year': year,
    #     'month': month,
    #     'lst_of_posts': lst
    # }
    # return render(request, 'blog/month_archive.html', context)
    pass


def day_archive(request, year, month, day):
    # lst = Post.objects.filter(
    #     created__year=year, created__month=month, created__day=day)
    # context = {
    #     'year': year,
    #     'month': month,
    #     'day': day,
    #     'lst_of_posts': lst
    # }
    # return render(request, 'blog/day_archive.html', context)
    pass


def post_key(request, key):
    pass


def thanks(request):
    # return HttpResponse("Your post has been submitted. Thank you!")
    pass


def add(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PostForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            author = form.cleaned_data['author']
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            published_date = timezone.now()
            # post_tags = form.cleaned_data['tags']

            Post.objects.create(
                author, title, content, published_date)
            # redirect to a new URL:
            return redirect('/')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = PostForm()

    return render(request, 'blog/add.html', {'form': form})

# # adding comments functionality
# def add_comment(request, post):
#     form = CommentForm(request.POST)
#     if form.is_valid():
#         author = form.cleaned_data['author']
#         content = form.cleaned_data['content']
#         post.comments.objects.create(author, content)
#     else:
#         form = CommentForm()
#
#     return render(request, 'blog/add_comment.html', {'form': form})


def index(request):
    list_of_posts = Post.objects.order_by('published_date')
    context = {
        'list_of_posts': list_of_posts
    }
    return render(request, 'blog/posts.html', context)


def about(request):
    return render(request, 'blog/about.html', {})


def archive(request):
    return render(request, 'blog/archive.html', {})


def contact(request):
    return render(request, 'blog/contact.html', {})
