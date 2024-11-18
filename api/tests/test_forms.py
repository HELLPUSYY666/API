from django.test import TestCase
from django.core.exceptions import ValidationError
from api.forms import UserForm, GroupForm, PostForm
from api.models import User, Group, Post


class TestForms(TestCase):

    def test_user_form_valid(self):
        form_data = {
            "email": "user1@example.com",
            "password": "Password123!",
            "first_name": "User1",
            "last_name": "Test",
            "mobile": "+1111111111",
            "date_joined": "2024-11-18T10:00:00Z"
        }
        form = UserForm(data=form_data)
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_user_form_invalid(self):
        form_data = {
            "email": "user1@example.com",
            "password": "Password123!",
            "first_name": "User1",
            "last_name": "Test",
            # "mobile" is missing
        }
        form = UserForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_group_form_valid(self):
        user = User.objects.create(
            email="user1@example.com",
            password="Password123!",
            first_name="User1",
            last_name="Test",
            mobile="+1111111111"
        )
        group_data = {
            "name": "Group1",
            "members": [user.id]
        }
        form = GroupForm(data=group_data)
        self.assertTrue(form.is_valid())

    def test_group_form_invalid(self):
        group_data = {
            "name": "Group1",
            # "members" is missing
        }
        form = GroupForm(data=group_data)
        self.assertFalse(form.is_valid())

    def test_post_form_valid(self):
        user = User.objects.create(
            email="user1@example.com",
            password="Password123!",
            first_name="User1",
            last_name="Test",
            mobile="+1111111111"
        )
        post_data = {
            "user": user.id,
            "title": "Post Title",
            "content": "Post Content"
        }
        form = PostForm(data=post_data)
        self.assertTrue(form.is_valid())

    def test_post_form_invalid(self):
        post_data = {
            # "user" is missing
            "title": "Post Title",
            "content": "Post Content"
        }
        form = PostForm(data=post_data)
        self.assertFalse(form.is_valid())
