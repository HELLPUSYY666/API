from django.test import TestCase
from django.core.exceptions import ValidationError
from api.models import *
from django.contrib.auth import get_user_model


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email="test@example.com",
            password="ValidPassword123!",
            first_name="John",
            last_name="Doe",
            mobile="+1234567890"
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("ValidPassword123!"))
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.mobile, "+1234567890")

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(
            email="admin@example.com",
            password="SuperPassword123!",
            first_name="Admin",
            last_name="User",
            mobile="+9876543210"
        )
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)


class ProfileModelTest(TestCase):
    def test_create_profile(self):
        user = get_user_model().objects.create_user(
            email="testuser@example.com",
            password="Password123!",
            first_name="Test",
            last_name="User",
            mobile="+1234567890"
        )
        profile = Profile.objects.create(user=user)
        self.assertEqual(profile.user, user)


class PostModelTest(TestCase):
    def test_create_post(self):
        user = get_user_model().objects.create_user(
            email="testuser@example.com",
            password="Password123!",
            first_name="Test",
            last_name="User",
            mobile="+1234567890"
        )
        post = Post.objects.create(
            user=user,
            title="Test Post",
            content="This is a test post."
        )
        self.assertEqual(post.title, "Test Post")
        self.assertEqual(post.content, "This is a test post.")


class GroupModelTest(TestCase):
    def test_create_group(self):
        user1 = get_user_model().objects.create_user(
            email="user1@example.com",
            password="Password123!",
            first_name="User1",
            last_name="Test",
            mobile="+1111111111"
        )
        user2 = get_user_model().objects.create_user(
            email="user2@example.com",
            password="Password123!",
            first_name="User2",
            last_name="Test",
            mobile="+2222222222"
        )
        group = Group.objects.create(name="Test Group")
        group.members.add(user1, user2)
        self.assertEqual(group.members.count(), 2)
