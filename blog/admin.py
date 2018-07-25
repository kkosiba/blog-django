from django.contrib import admin

from .models import Category
from .models import Post
from .models import Comment


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'author', 'title', 'slug', 'status', 'created_date', )
    list_filter = (
        'status', 'created_date', 'published_date', 'author', )
    search_fields = ('title', 'author', )
    prepopulated_fields = {'slug': ('title', ), }
    raw_id_fields = ('author', )
    date_hierachy = 'published_date'
    ordering = ['status', 'published_date', ]


# Register your models here.
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
