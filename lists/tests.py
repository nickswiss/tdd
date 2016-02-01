from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import home_page
from django.http import HttpRequest

# Create your tests here.
class HomePageTest(TestCase):

    def test_root_url_resolves(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>To-Do Lists</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))

