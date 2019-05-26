from django import template
import calendar

register = template.Library()

@register.filter
def month_name(month_number):
    """
    Filter converting numeric value of month to text value
    """
    return calendar.month_name[month_number]

@register.filter
def shorten_post(content):
    words = content.split(' ')[:15]
    return ' '.join(words) + '...'

@register.filter
def paginate(paginator, current_page, neighbors=10):
    if paginator.num_pages > 2 * neighbors:
        start_index = max(1, current_page-neighbors)
        end_index = min(paginator.num_pages, current_page + neighbors)
        if end_index < start_index + 2 * neighbors:
            end_index = start_index + 2 * neighbors
        elif start_index > end_index - 2 * neighbors:
            start_index = end_index - 2 * neighbors
        if start_index < 1:
            end_index -= start_index
            start_index = 1
        elif end_index > paginator.num_pages:
            start_index -= (end_index-paginator.num_pages)
            end_index = paginator.num_pages
        page_list = [f for f in range(start_index, end_index + 1)]
        return page_list[:(2 * neighbors + 1)]
    return paginator.page_range

@register.simple_tag
def url_replace(request, field, value):
    query_string = request.GET.copy()
    query_string[field] = value
    
    return query_string.urlencode()