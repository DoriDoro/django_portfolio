from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from accounts.models import Profile

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


class ProfileModelTestCase(ModelTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.profile = Profile(
            user=cls.user,
            phone_number_en="+49 30 123456",
            address_en="Berlin, Germany",
            profession_en="Software Developer",
            motto_en="Keep it simple",
            introduction_en="<p>Hello world</p>",
            more_details_en="<p>More about me</p>",
        )
        cls.profile.save(clean=False)

    def test_str(self):
        self.assertEqual(str(self.profile), self.USERNAME)

    def test_normalize_strips_whitespace(self):
        profile = Profile(
            user=UserModel.objects.create_user(
                username="Spacey", email="spacey@mail.com", password=self.USER_PASSWORD
            ),
            phone_number_en="  +49 30 000  ",
            address_en="  Munich  ",
            profession_en="  Engineer  ",
            motto_en="  Never stop  ",
            introduction_en="<p>Hello</p>",
            more_details_en="<p>Details</p>",
        )
        profile.save(clean=False)
        self.assertEqual(profile.phone_number_en, "+49 30 000")
        self.assertEqual(profile.address_en, "Munich")
        self.assertEqual(profile.profession_en, "Engineer")
        self.assertEqual(profile.motto_en, "Never stop")

    def test_blank_introduction_raises_validation_error(self):
        profile = Profile(
            user=UserModel.objects.create_user(
                username="NoIntro", email="nointro@mail.com", password=self.USER_PASSWORD
            ),
            phone_number_en="+49 30 000",
            address_en="Munich",
            profession_en="Engineer",
            motto_en="Never stop",
            introduction_en="",
            more_details_en="<p>Details</p>",
        )
        with self.assertRaises(ValidationError):
            profile.full_clean()

    def test_save_clean_false_skips_validation(self):
        profile = Profile(
            user=UserModel.objects.create_user(
                username="SkipClean", email="skip@mail.com", password=self.USER_PASSWORD
            ),
            phone_number_en="",
            address_en="",
            profession_en="",
            motto_en="",
            introduction_en="",
            more_details_en="",
        )
        profile.save(clean=False)

    def test_linked_via_user(self):
        self.assertEqual(self.user.profile, self.profile)
