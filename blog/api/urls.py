from django.urls import path, include
from rest_framework.routers import DefaultRouter


from blog.api.views import PostViewSet, UserViewSet

# Create a router and register viewsets with it.
router = DefaultRouter()
router.register(r"posts", PostViewSet)
router.register(r"users", UserViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [path("", include(router.urls))]


# path('add/', AddPost.as_view(), name='add_post'),

# path('add/drafts/', PostDraftsList.as_view(), name='list_drafts'),

# path('search/', SearchPosts.as_view(), name='search'),

# # post archives
# path('<int:year>/',
#      PostYearArchive.as_view(), name='y_archive'),
# path('<int:year>/<int:month>/',
#      PostYearMonthArchive.as_view(month_format='%m'), name='ym_archive'),

# path('tag/<str:tag>/', ListByTag.as_view(), name='tag'),
# path('category/<str:name>/', ListByCategory.as_view(), name='category'),
# path('author/<str:author>/', ListByAuthor.as_view(), name='author'),

# path('<slug:slug>/', DetailsPost.as_view(), name='details_post'),
# path('<slug:slug>/delete/', DeletePost.as_view(), name='delete_post'),
# path('<slug:slug>/update/', UpdatePost.as_view(), name='update_post'),

