from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from api.models import *
import json
from rest_framework.test import APIClient, APITestCase


class TestViewsGET(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(password='testpassword', email='pzakakaak@mail.ru',
                                             first_name='Jhon', last_name='Smith', mobile='87002005123')
        self.client.force_authenticate(user=self.user)

    def test_project_list_GET(self):
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, 200)


class TestViewsPOST(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(password='testpassword', email='pzakakaak@mail.ru',
                                             first_name='Jhon', last_name='Smith', mobile='87002005123')
        self.client.force_authenticate(user=self.user)

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
        self.assertIn("id", response.data)

    def test_create_user_duplicate_email_POST(self):
        User.objects.create_user(
            email="duplicate@mail.com",
            password="password123",
            first_name="Duplicate",
            last_name="User",
            mobile="87002005555"
        )

        data = {
            "email": "duplicate@mail.com",
            "password": "newpassword",
            "first_name": "New",
            "last_name": "User",
            "mobile": "87002005555"
        }
        response = self.client.post(reverse('user-create'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.data)

    def test_create_user_invalid_email_POST(self):
        data = {
            "email": "notanemail",
            "password": "securepassword",
            "first_name": "Invalid",
            "last_name": "Email",
            "mobile": "87002005555"
        }
        response = self.client.post(reverse('user-create'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.data)

    def test_create_user_missing_password_POST(self):
        data = {
            "email": "newuser@mail.com",
            "first_name": "No",
            "last_name": "Password",
            "mobile": "87002005555"
        }
        response = self.client.post(reverse('user-create'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("password", response.data)

    def test_create_user_long_name_POST(self):
        data = {
            "email": "longname@mail.com",
            "password": "securepassword",
            "first_name": "A" * 300,
            "last_name": "User",
            "mobile": "87002005555"
        }
        response = self.client.post(reverse('user-create'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("first_name", response.data)


class UserUpdateTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@mail.com",
            password="password123",
            first_name="Test",
            last_name="User",
            mobile="87001234567"
        )
        self.url = reverse('user-detail', kwargs={'pk': self.user.id})

    def test_update_user(self):
        data = {
            "email": "updateduser@mail.com",
            "first_name": "Updated",
            "last_name": "Name",
            "mobile": "87002006666",
            "password": "olgaria"
        }

        login_data = {
            'email': 'testuser@mail.com',
            'password': 'password123'
        }

        login_response = self.client.post(reverse('token_obtain_pair'), login_data, format='json')

        self.assertIn('access', login_response.data)
        token = login_response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.put(self.url, data, format='json')

        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertEqual(self.user.email, data["email"])
        self.assertEqual(self.user.first_name, data["first_name"])
        self.assertEqual(self.user.last_name, data["last_name"])
        self.assertEqual(self.user.mobile, data["mobile"])


class UserDeleteTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@mail.com",
            password="password123",
            first_name="Test",
            last_name="User",
            mobile="87001234567"
        )
        self.url = reverse('user-delete', kwargs={'pk': self.user.id})

    def test_delete_user(self):
        login_data = {
            'email': 'testuser@mail.com',
            'password': 'password123'
        }

        login_response = self.client.post(reverse('token_obtain_pair'), login_data, format='json')
        self.assertIn('access', login_response.data)
        token = login_response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        self.assertTrue(User.objects.filter(id=self.user.id).exists())

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(User.objects.filter(id=self.user.id).exists())

    def test_delete_nonexistent_user(self):
        login_data = {
            'email': 'testuser@mail.com',
            'password': 'password123'
        }

        login_response = self.client.post(reverse('token_obtain_pair'), login_data, format='json')
        self.assertIn('access', login_response.data)
        token = login_response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = reverse('user-delete', kwargs={'pk': 99999})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



