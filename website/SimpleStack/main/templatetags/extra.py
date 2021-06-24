from django import template
from django.utils.safestring import SafeString
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def subtract(value):
    print("value: " + value)
    return int(value) - 1

@register.filter(is_safe=True)
@stringfilter
def add(value):
    print("value: " + value)
    return int(value) + 1