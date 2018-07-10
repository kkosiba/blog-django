from django.contrib import admin
from .models import Post, Author

# Register your models here.
admin.site.register(Author)
admin.site.register(Post)
