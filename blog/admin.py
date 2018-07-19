from django.contrib import admin

from .models import Category
from .models import Post
from .models import Comment

# Register your models here.
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
