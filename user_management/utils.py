from django.urls import reverse, NoReverseMatch

def reverse_without_namespace(viewname, *args, **kwargs):
    try:
        # Try reversing with the namespace
        return reverse(viewname, *args, **kwargs)
    except NoReverseMatch:
        # If it fails, try reversing without the namespace
        viewname = viewname.split(':')[-1]
        return reverse(viewname, *args, **kwargs)