from django import template

register = template.Library()

@register.simple_tag
def noscript_warning():
    return '''
    <noscript>
        <div style="background-color: red; color: white; padding: 10px; text-align: center;">
            JavaScript is required for this website to function properly. Please enable JavaScript in your browser settings.
        </div>
    </noscript>
    '''
