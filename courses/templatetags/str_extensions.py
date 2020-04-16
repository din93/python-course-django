from django import template

register = template.Library()

def capitalize(str_input):
    return str_input.capitalize()

register.filter('capitalize', capitalize)