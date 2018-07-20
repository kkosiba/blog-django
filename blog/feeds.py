from django.contrib.syndication.views import Feed
from django.urls import reverse
from blog.models import Post


class LastEntriesFeed(Feed):
    title = 'Latest posts'
    link = '/'
    description = 'Latest posts'

    def items(self):
        return Post.objects.order_by('-published_date')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    # needed because Post has no get_absolute_url method
    def item_link(self, item):
        return reverse('single_post', args=[item.pk])
