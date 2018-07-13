from django.urls import path

from . import views

urlpatterns = [
    # path('<int:year>/', views.years_archive),
    # path('<int:year>/<int:month>/', views.month_archive),
    # path('<int:year>/<int:month>/<int:day>/', views.day_archive),
    path('post/add/', views.add, name='add'),
    path('contact/', views.contact, name='contact'),
    path('archive/', views.archive, name='archive'),
    path('about/', views.about, name='about'),
    path('', views.index, name='index'),
]
