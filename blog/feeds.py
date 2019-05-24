from django.contrib.syndication.views import Feed
from blog.models import Post


class LastEntriesFeed(Feed):
    title = "Latest posts"
    link = "/"
    description = "Latest posts"

    def items(self):
        return Post.objects.order_by("-published_date")

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        words = item.content.split(" ")[:10]
        return " ".join(words) + "..."
