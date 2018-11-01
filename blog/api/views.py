from rest_framework import generics, permissions
from .permissions import IsOwnerOrReadOnly

from blog.models import Post
from django.contrib.auth.models import User
from .serializers import (
    PostSerializer,
    UserSerializer,
    )

from .pagination import (
    PostPageNumberPagination,
    UserPageNumberPagination,
    )

from rest_framework.viewsets import (
    ModelViewSet,
    ReadOnlyModelViewSet,
    )

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
    )

from django.shortcuts import get_object_or_404

# for later use
# class MultipleFieldLookupMixin(object):
#     """
#     Apply this mixin to any view or viewset to get multiple field filtering
#     based on a `lookup_fields` attribute, instead of the default single field filtering.
#     """
#     def get_object(self):
#         queryset = self.get_queryset()             # Get the base queryset
#         queryset = self.filter_queryset(queryset)  # Apply any filter backends
#         filter = {}
#         for field in self.lookup_fields:
#             if self.kwargs[field]: # Ignore empty fields.
#                 filter[field] = self.kwargs[field]
#         obj = get_object_or_404(queryset, **filter)  # Lookup the object
#         self.check_object_permissions(self.request, obj)
#         return obj


class PostViewSet(ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly, )
    lookup_field = 'slug'

    filter_backends = [SearchFilter, OrderingFilter, ]
    search_fields = ['category__name',
                     'author__first_name',
                     'title',
                     'content', ]

    pagination_class = PostPageNumberPagination

    # doesn't save to the database...
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    filter_backends = [SearchFilter, OrderingFilter, ]
    search_fields = ['first_name']

    pagination_class = UserPageNumberPagination
