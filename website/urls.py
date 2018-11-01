"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

from blog.views import (
    Contact, SignUp, UpdateProfile,
    )

from blog.feeds import LastEntriesFeed

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', SignUp.as_view(), name='signup'),
    path('accounts/profile/', UpdateProfile.as_view(), name='profile'),

    path('contact/', Contact.as_view(), name='contact'),
    path('latest/feed/', LastEntriesFeed(), name='feed'),
   
    path('api/', include('blog.api.urls')), # REST api
    path('', include('blog.urls')),
    path('markdownx/', include('markdownx.urls')),
]

# to load static/media files in development environment
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
