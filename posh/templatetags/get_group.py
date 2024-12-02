from django import template
from django.contrib.auth.models import Group 

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name): 
    return user.groups.filter(name=group_name).exists()


@register.filter(name='abs')
def abs_value(value):
    """Returns the absolute value of a number."""
    try:
        return abs(int(value))
    except (ValueError, TypeError):
        return value