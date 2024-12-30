from django import template


register = template.Library()


@register.filter
def seconds(obj):
    return int(obj.total_seconds())
