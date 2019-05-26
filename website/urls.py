from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from posts.feeds import LastEntriesFeed

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("contact/", include("contact.urls", namespace="contact")),
    path("latest/feed/", LastEntriesFeed(), name="feed"),
    path("api/", include("posts.api.urls")),  # REST api
    path("", include("posts.urls")),
    path("markdownx/", include("markdownx.urls")),
]

# to load static/media files in development environment
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
