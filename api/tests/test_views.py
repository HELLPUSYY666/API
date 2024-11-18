from django.test import TestCase, Client
from django.urls import reverse
from api.models import *
import json
from rest_framework.test import APIClient


class TestViews(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(password='testpassword', email='pzakakaak@mail.ru',
                                             first_name='Jhon', last_name='Smith', mobile='87002005123')
        self.client.force_authenticate(user=self.user)

    def test_project_list_GET(self):
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, 200)

    def test_project_list_POST(self):
        data = {
            "email": "newuser@mail.com",
            "password": "newpassword",
            "first_name": "New",
            "last_name": "User",
            "mobile": "87002005555"
        }
        response = self.client.post(reverse('user-create'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

