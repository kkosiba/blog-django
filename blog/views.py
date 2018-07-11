from django.shortcuts import render
from django.http import HttpResponse
from .models import Post

# Create your views here.


def years_archive(request, year):
    lst = Post.objects.filter(created__year=year)
    context = {
        'year': year,
        'lst_of_posts': lst
    }
    return render(request, 'blog/years_archive.html', context)


def month_archive(request, year, month):
    lst = Post.objects.filter(created__year=year, created__month=month)
    context = {
        'year': year,
        'month': month,
        'lst_of_posts': lst
    }
    return render(request, 'blog/month_archive.html', context)


def day_archive(request, year, month, day):
    lst = Post.objects.filter(
        created__year=year, created__month=month, created__day=day)
    context = {
        'year': year,
        'month': month,
        'day': day,
        'lst_of_posts': lst
    }
    return render(request, 'blog/day_archive.html', context)


def post_key(request, key):
    pass


def index(request):
    return HttpResponse("Welcome to the main page!")
