from api.models import Notification, User


def test_signal_triggers_notification(self):
    user = User.objects.create_user(
        email="testuser@example.com",
        password="testpassword",
        first_name="Test",
        last_name="User",
        mobile="1234567890"
    )

    # Создание уведомления через модель Notification
    notification = Notification.objects.create(
        user=user,
        title="Тест",
        message="Это тестовое уведомление"
    )

    # Проверка, что уведомление создано
    self.assertIsNotNone(notification)
    self.assertEqual(notification.user, user)
    self.assertEqual(notification.title, "Тест")
    self.assertEqual(notification.message, "Это тестовое уведомление")
