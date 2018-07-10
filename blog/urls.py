from django.urls import path

from . import views

urlpatterns = [
    path('posts/<int:year>/', views.years_archive),
    path('posts/<int:year>/<int:month>/', views.month_archive),
    path('posts/<int:year>/<int:month>/<int:key>/', views.post_detail),
    path('', views.index, name='index'),
]
