from django import template

register = template.Library()

@register.tag
def sowner(i,j):
    return "hello"
