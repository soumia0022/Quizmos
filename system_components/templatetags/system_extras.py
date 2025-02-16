from django import template

register = template.Library()

#  For the information buttons
@register.inclusion_tag('info_button.html')
def info_button(info_text):
    return {'info_text': info_text}

#  For the return to dashboard buttons
@register.inclusion_tag('return_button.html')
def return_button():
    return {}

#  For the return to the previous page button
@register.inclusion_tag('go_back_button.html')
def go_back_button():
    return {}

# For the JavaScript restriction warning
@register.inclusion_tag('noscript_warning.html')
def noscript_warning():
    return {}