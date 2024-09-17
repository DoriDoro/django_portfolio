from datetime import datetime

from django.contrib.auth import get_user_model
from unittest import TestCase

from doridoro.models import DoriDoro
from projects.models import Project

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

    # Project attributes
    P_TITLE = "Test Project title"
    P_SLUG = "test-project-title"
    P_LEGEND = "Test Project legend"
    P_CREATE_DATE = datetime.now()
    P_INTRODUCTION = "Test Project introduction"
    P_CONTENT = "Test Project content"
    P_TAGS = "PERSONAL_PROJECT"
    P_DORIDORO = "Test Project doridoro"

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
        cls.project = Project.objects.create(
            title=cls.P_TITLE,
            slug=cls.P_SLUG,
            legend=cls.P_LEGEND,
            create_date=cls.P_CREATE_DATE,
            introduction=cls.P_INTRODUCTION,
            content=cls.P_CONTENT,
            tags=cls.P_TAGS,
            doridoro=cls.P_DORIDORO,
        )


# class ProjectTestCase(ModelTestCase):
#     def test_project_creation_successful(self):
#         self.assertIsNotNone(self.project, "Project instance was not created")
#         self.assertEqual(self.project.title, self.P_TITLE)
#         self.assertEqual(self.project.legend, self.P_LEGEND)
#         self.assertEqual(self.project.introduction, self.P_INTRODUCTION)
#         self.assertEqual(self.project.content, self.P_CONTENT)
#         self.assertEqual(self.project.doridoro, self.P_DORIDORO)
