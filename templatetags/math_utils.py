from django import template

register = template.Library()


@register.filter(name="abs")
def abs_value(value):
    return abs(value)


@register.filter(name="is_negative")
def is_negative(value):
    return value < 0
