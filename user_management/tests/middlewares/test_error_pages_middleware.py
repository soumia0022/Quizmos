from django.test import TestCase
from django.core.exceptions import PermissionDenied
from django.test.client import RequestFactory
from django.conf import settings
from user_management.middleware import CustomErrorMiddleware


class CustomErrorMiddlewareTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = CustomErrorMiddleware(get_response=self.fake_get_response)

    def fake_get_response(self, request):
        """Fake response method for testing middleware"""
        return self.client.get('/')

    def test_process_exception_renders_403_template(self):
        request = self.factory.get('/some-url/')
        exception = PermissionDenied("Permission denied")

        response = self.middleware.process_exception(request, exception)

        self.assertEqual(response.status_code, 403)
        self.assertIn(b"403", response.content)

    def test_process_exception_renders_500_template_debug_on(self):


        request = self.factory.get('/some-url/?custom_error=1')
        exception = Exception("Some internal server error")

        response = self.middleware.process_exception(request, exception)


        self.assertEqual(response.status_code, 500)
        self.assertIn(b"500", response.content)

    def test_process_exception_renders_500_template_debug_off(self):
        settings.DEBUG = False

        request = self.factory.get('/some-url/')
        exception = Exception("Some internal server error")

        response = self.middleware.process_exception(request, exception)


        self.assertEqual(response.status_code, 500)
        self.assertIn(b"500", response.content)
