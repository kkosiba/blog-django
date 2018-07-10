from django.shortcuts import render
from .models import Post

# Create your views here.


def years_archive(request, year):
    lst = Post.objects.filter(published__year=year)
    context = {
        'year': year,
        'lst_of_posts': lst
    }
    return render(request, 'blog/years_archive.html', context)


def index(request):
    return HttpResponse("Welcome to the main page!")
