from django import template
import calendar

register = template.Library()

@register.filter
def month_name(month_number):
    """
    Filter converting numeric value of month to text value
    """
    return calendar.month_name[month_number]