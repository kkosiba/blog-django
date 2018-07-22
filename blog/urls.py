from django.contrib.auth import views as auth_views
from django.urls import path
from blog.feeds import LastEntriesFeed

from . import views

urlpatterns = [
    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('search/', views.search, name='search'),
    path('category 1/', views.category1, name='category1'),
    path('category 2/', views.category2, name='category2'),
    path('category 3/', views.category3, name='category3'),
    path('category 4/', views.category4, name='category4'),
    path('category 5/', views.category5, name='category5'),
    path('add/', views.add, name='add'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('', views.index, name='index'),
    path('archive/<int:year>/<int:month>/', views.year_month, name='year_month'),
    path('archive/<int:year>/', views.year, name='year'),
    path('post/<int:pk>/', views.single_post, name='single_post'),
    # path('post/<int:pk>/add_comment/', views.add_comment, name='add_comment'),
    path('latest/feed/', LastEntriesFeed()),
]
