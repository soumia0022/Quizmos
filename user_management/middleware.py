from django.http import Http404
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.conf import settings


class Custom404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            return render(request, '404.html', status=404)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, Http404):
            return render(request, '404.html', status=404)
        return None


class CustomErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        return response

    def process_exception(self, request, exception):
        """Handle specific exceptions and render appropriate error templates"""
        if isinstance(exception, PermissionDenied):
            return render(request, '403.html', {
                'exception': exception,
                'debug': settings.DEBUG
            }, status=403)


        if settings.DEBUG:
            show_custom_500 = request.GET.get('custom_error') == '1'
            if show_custom_500:
                return render(request, '500.html', {
                    'exception': exception,
                    'debug': True
                }, status=500)
            return None
        else:
            return render(request, '500.html', {
                'exception': exception,
                'debug': False
            }, status=500)

        return None