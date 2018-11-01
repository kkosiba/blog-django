from rest_framework.pagination import PageNumberPagination

class PostPageNumberPagination(PageNumberPagination):
    """
    Custom pagination for posts
    """
    page_size = 1 # for testing


class UserPageNumberPagination(PageNumberPagination):
    """
    Custom pagination for users
    """
    page_size = 1 # for testing
