from django import template

register = template.Library()

@register.inclusion_tag('info_button.html')
def info_button(info_text):
    return {'info_text': info_text}
