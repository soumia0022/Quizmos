from django.test import TestCase
from django.http import Http404
from django.test.client import RequestFactory
from user_management.middleware import Custom404Middleware


class Custom404MiddlewareTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = Custom404Middleware(get_response=self.fake_get_response)

    def fake_get_response(self, request):
        """Fake response method for testing middleware"""
        return self.client.get('/non-existent-url/')

    def test_404_middleware_renders_404_template(self):

        request = self.factory.get('/non-existent-url/')
        response = self.middleware.__call__(request)


        self.assertEqual(response.status_code, 404)
        self.assertIn(b"404", response.content)

    def test_process_exception_renders_404_template(self):
        request = self.factory.get('/any-url/')
        exception = Http404("Page not found")

        response = self.middleware.process_exception(request, exception)

        self.assertEqual(response.status_code, 404)
        self.assertIn(b"404", response.content)
