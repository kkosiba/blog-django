from django.contrib.auth import views as auth_views
from django.urls import path
from blog.feeds import LastEntriesFeed

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # user management
    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),

    # posts related
    path('post/<slug:slug>/', views.single_post, name='single_post'),
    path('posts/<int:year>/', views.year, name='year'),
    path('posts/<int:year>/<int:month>/', views.year_month, name='year_month'),
    path('posts/category 1/', views.category1, name='Category 1'),
    path('posts/category 2/', views.category2, name='Category 2'),
    path('posts/category 3/', views.category3, name='Category 3'),
    path('posts/add/', views.add, name='add'),
    path('posts/search/', views.search, name='search'),

    # misc
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('latest/feed/', LastEntriesFeed()),
]
