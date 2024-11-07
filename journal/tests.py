from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from doridoro.models import DoriDoro
from journal.models import Journal

UserModel = get_user_model()


class ModelTestCase(TestCase):
    # User attributes
    USERNAME = "TestUser"
    USER_EMAIL = "testuser_project@mail.com"
    USER_PASSWORD = "TestProjectW0rd!"

    # DoriDoro attributes
    D_PHONE = "987654321"
    D_ADDRESS = "Test address - Project"
    D_PROFESSION = "Test profession text - Project"
    D_INTRODUCTION = "Test introduction text - Project"
    D_DREAM_JOB = "Test dream job text - Project"
    D_FREE_TIME = "Test free time text - Project"

    # Journal attributes
    NAME = "Test-Journal"
    TITLE = "Test Name"
    SLUG = "test-name"
    CONTENT = "Test content"
    CREATED = datetime.now()
    UPDATED = datetime.now()
    STATUS = "PUBLISHED"

    @classmethod
    def setUpTestData(cls):
        cls.user = UserModel.objects.create_user(
            username=cls.USERNAME, email=cls.USER_EMAIL, password=cls.USER_PASSWORD
        )
        cls.doridoro = DoriDoro.objects.create(
            user=cls.user,
            phone=cls.D_PHONE,
            address=cls.D_ADDRESS,
            profession=cls.D_PROFESSION,
            introduction=cls.D_INTRODUCTION,
            dream_job=cls.D_DREAM_JOB,
            free_time=cls.D_FREE_TIME,
        )
        cls.journal = Journal.objects.create(
            name=cls.NAME,
            title=cls.TITLE,
            slug=cls.SLUG,
            content=cls.CONTENT,
            created=cls.CREATED,
            updated=cls.UPDATED,
            status=cls.STATUS,
            author=cls.user,
        )
