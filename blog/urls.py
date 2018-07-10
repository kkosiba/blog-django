from django.urls import path

from . import views

urlpatterns = [
    path('posts/<int:year>/', views.years_archive),
    path('posts/<int:year>/<int:month>/', views.month_archive),
    path('posts/<int:year>/<int:month>/<int:day>/', views.day_archive),
    path('posts/<int:post_key>', views.post_key),
    path('', views.index, name='index'),
]
