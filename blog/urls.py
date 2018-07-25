from django.contrib.auth import views as auth_views
from django.urls import path
from blog.feeds import LastEntriesFeed

# for restricting access to post related actions
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    # user management
    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),

    # posts related
    path('', views.ListPostsView.as_view(), name='index'),
    path('post/<slug:slug>/',
         views.DetailsPostView.as_view(), name='single_post'),
    path('posts/<int:year>/',
         views.ListPostsByYearView, name='year'),
    path('posts/<int:year>/<int:month>/',
         views.ListPostsByYearMonthView.as_view(), name='year_month'),
    path('posts/category/<str:name>/', views.category, name='category'),
    path('posts/add/',
         login_required(views.AddPostView.as_view()), name='add_post'),
    path('posts/<slug:slug>/delete/',
         login_required(views.DeletePostView.as_view()), name='delete_post'),
    path('posts/<slug:slug>/update/',
         login_required(views.UpdatePostView.as_view()), name='update_post'),
    path('posts/search/', views.search, name='search'),

    # misc
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('latest/feed/', LastEntriesFeed()),
]
