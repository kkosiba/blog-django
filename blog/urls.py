from django.urls import path

from .views import (
    PostYearArchive, PostYearMonthArchive, PostYearMonthDayArchive,
    ListPosts, DetailsPost, PostDraftsList, SearchPosts,
    AddPost, DeletePost, UpdatePost,
    ListTags, ListByTag,
    ListCategories, ListByCategory,
    ListAuthors, ListByAuthor,
    )

app_name = 'blog'

urlpatterns = [
    path('', ListPosts.as_view(), name='index'),
    path('add/', AddPost.as_view(), name='add_post'),

    # not yet implemented
    path('add/drafts/', PostDraftsList.as_view(), name='list_drafts'),

    path('search/', SearchPosts.as_view(), name='search'),
    
    # post archives
    path('<int:year>/',
         PostYearArchive.as_view(), name='y_archive'),
    path('<int:year>/<int:month>/',
         PostYearMonthArchive.as_view(month_format='%m'), name='ym_archive'),
    path('<int:year>/<int:month>/<int:day>/',
         PostYearMonthDayArchive.as_view(month_format='%m'),
         name='ymd_archive'),
    
    path('tags/', ListTags.as_view(), name='tags'),
    path('tags/<str:tag>/', ListByTag.as_view(), name='tag'),

    path('category/', ListCategories.as_view(), name='all_categories'),
    path('category/<str:name>/', ListByCategory.as_view(), name='category'),
    
    path('author/', ListAuthors.as_view(), name='authors'),
    path('author/<str:author>/', ListByAuthor.as_view(), name='author'),
    
    path('<slug:slug>/', DetailsPost.as_view(), name='details_post'),
    path('<slug:slug>/delete/', DeletePost.as_view(), name='delete_post'),
    path('<slug:slug>/update/', UpdatePost.as_view(), name='update_post'),
]