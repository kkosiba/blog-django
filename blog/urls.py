from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('post/add/', views.add, name='add'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('', views.index, name='index'),
]
