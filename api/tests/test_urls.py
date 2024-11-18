from django.test import SimpleTestCase
from django.urls import reverse, resolve
from djoser.views import UserViewSet as DjoserUserViewSet
from api.views import UserViewSet as CustomUserViewSet


class TestUrls(SimpleTestCase):
    def test_list_url_is_resolved(self):
        url = reverse('user-list')
        self.assertEqual(resolve(url).func.cls, DjoserUserViewSet)
        self.assertEqual(resolve(url).view_name, 'user-list')

    def test_create_url_is_resolved(self):
        url = reverse('user-create')
        self.assertEqual(resolve(url).func.cls, CustomUserViewSet)
        self.assertEqual(resolve(url).view_name, 'user-create')

    def test_detail_url_is_resolved(self):
        url = reverse('user-detail', args=['1'])
        self.assertEqual(resolve(url).func.cls, DjoserUserViewSet)


