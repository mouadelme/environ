from django.test import SimpleTestCase
from django.urls import resolve, reverse
from whistleblower.views import home, logout_view, upload_form


class test_urls(SimpleTestCase):

    def test_home_url_is_resolved(self):
       url = reverse('home')
       self.assertTrue(resolve(url))

    def test_logout_url_is_resolved(self):
        url = reverse('logout')
        self.assertTrue(resolve(url))

    def test_upload_url_is_resolved(self):
        url = reverse('upload_form')
        self.assertTrue(resolve(url))

    def test_files_is_resolved(self):
        url = reverse('files')
        self.assertTrue(resolve(url))
