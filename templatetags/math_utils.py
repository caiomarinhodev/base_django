from django import template

register = template.Library()


@register.filter(name="abs")
def abs_value(value):
    return abs(int(value))


@register.filter(name="is_negative")
def is_negative(value):
    return int(value) < 0
