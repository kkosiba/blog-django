from django.urls import path
from blog.feeds import LastEntriesFeed

from . import views

urlpatterns = [
    path('category 1/', views.category1, name='category1'),
    path('category 2/', views.category2, name='category2'),
    path('category 3/', views.category3, name='category3'),
    path('category 4/', views.category4, name='category4'),
    path('category 5/', views.category5, name='category5'),
    path('signup/', views.signup, name='signup'),
    path('add/', views.add, name='add'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('', views.index, name='index'),
    path('post/<int:pk>/', views.single_post, name='single_post'),
    path('latest/feed/', LastEntriesFeed()),
]
