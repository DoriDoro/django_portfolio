from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase


UserModel = get_user_model()


class ModelTestCase(TestCase):
    USERNAME = "TestUser"
    USER_EMAIL = "testuser@mail.com"
    USER_PASSWORD = "TestPassw0rd!"

    @classmethod
    def setUpTestData(cls):
        cls.user = UserModel.objects.create_user(
            username=cls.USERNAME, email=cls.USER_EMAIL, password=cls.USER_PASSWORD
        )


class UserModelTestCase(ModelTestCase):
    def test_user_creation_successful(self):
        UserModel.objects.create_user(
            username="TestUser2",
            email="testuser2@mail.com",
            password=self.USER_PASSWORD,
        )

    def test_user_creation_failed(self):
        invalid_data = [
            {"username": "", "email": "", "password": None},
            {"username": None, "email": "testuser3@mail.com", "password": ""},
            {"username": "", "email": None, "password": self.USER_PASSWORD},
        ]

        for data in invalid_data:
            with self.assertRaises(ValueError):
                UserModel.objects.create_user(**data)

    def test_user_creation_second_time(self):
        with self.assertRaises(IntegrityError):
            UserModel.objects.create_user(
                username=self.USERNAME,
                email=self.USER_EMAIL,
                password=self.USER_PASSWORD,
            )
