from django.contrib.auth import get_user_model
from django.test import TestCase

from doridoro.models import (
    DoriDoro,
    Achievement,
    Degree,
    Fact,
    Hobby,
    Job,
    Language,
    SocialMedia,
    Reference,
)

UserModel = get_user_model()


class ModelTestCase(TestCase):
    # User attributes
    USERNAME = "TestUser"
    USER_EMAIL = "testuser@mail.com"
    USER_PASSWORD = "TestPassw0rd!"

    # DoriDoro attributes
    D_PHONE = "123456789"
    D_ADDRESS = "Test address"
    D_PROFESSION = "Test profession text"
    D_INTRODUCTION = "Test introduction text"
    D_DREAM_JOB = "Test dream job text"
    D_FREE_TIME = "Test free time text"

    # Achievement attributes
    A_TITLE = "Test achievement title"
    A_CONTENT = "Test achievement content"

    # Degree attributes
    DE_ORGANIZATION = "Test degree organization"
    DE_DEGREE = "Test degree"

    # Fact attributes
    F_TITLE = "Test Fact title"
    F_CONTENT = "Test Fact content"

    # Hobby attributes
    H_NAME = "Test Hobby name"

    # Job attributes
    J_COMPANY_NAME = "Test Job company name"
    J_POSITION = "Test Job position"
    J_START_DATE = "2023-01-01"
    J_ADDRESS = "Test Job address"
    J_JOB_TYPE = "EMPLOYED"
    J_DESCRIPTION = "Test Job description"

    # Language attributes
    L_NAME = "Test Language name"
    L_LEVEL = "Test Language level"

    # Reference attributes
    R_NAME = "Test Reference name"
    R_PROFESSION = "Test Reference profession"
    R_EMAIL = "Test Reference email"
    R_PHONE = "Test Reference phone"
    R_LANGUAGE = "Test Reference language"

    # SocialMedia attributes
    S_NAME = "Test Social name"
    S_URL = "https://test-url"

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
        cls.achievement = Achievement.objects.create(
            title=cls.A_TITLE, content=cls.A_CONTENT
        )
        cls.degree = Degree.objects.create(
            organization=cls.DE_ORGANIZATION, degree=cls.DE_DEGREE
        )
        cls.fact = Fact.objects.create(title=cls.F_TITLE, content=cls.F_CONTENT)
        cls.hobby = Hobby.objects.create(name=cls.H_NAME)
        cls.job = Job.objects.create(
            company_name=cls.J_COMPANY_NAME,
            position=cls.J_POSITION,
            start_date=cls.J_START_DATE,
            address=cls.J_ADDRESS,
            job_type=cls.J_JOB_TYPE,
            description=cls.J_DESCRIPTION,
        )
        cls.language = Language.objects.create(name=cls.L_NAME, level=cls.L_LEVEL)
        cls.reference = Reference.objects.create(
            name=cls.R_NAME,
            profession=cls.R_PROFESSION,
            email=cls.R_EMAIL,
            phone=cls.R_PHONE,
            language=cls.R_LANGUAGE,
        )
        cls.socialmedia = SocialMedia.objects.create(name=cls.S_NAME, url=cls.S_URL)


class DoriDoroTestCase(ModelTestCase):
    def test_doridoro_creation_successful(self):
        self.assertEqual(self.doridoro.phone, self.D_PHONE)
        self.assertEqual(self.doridoro.user.username, self.USERNAME)
        self.assertEqual(self.doridoro.user.email, self.USER_EMAIL)
        self.assertEqual(self.doridoro.profession, self.D_PROFESSION)
        self.assertEqual(self.doridoro.address, self.D_ADDRESS)
        self.assertEqual(self.doridoro.introduction, self.D_INTRODUCTION)
        self.assertEqual(self.doridoro.dream_job, self.D_DREAM_JOB)
        self.assertEqual(self.doridoro.free_time, self.D_FREE_TIME)


class AchievementTestCase(ModelTestCase):
    def test_achievement_creation_successful(self):
        self.assertEqual(self.achievement.title, self.A_TITLE)
        self.assertEqual(self.achievement.content, self.A_CONTENT)


class DegreeTestCase(ModelTestCase):
    def test_degree_creation_successful(self):
        self.assertEqual(self.degree.organization, self.DE_ORGANIZATION)
        self.assertEqual(self.degree.degree, self.DE_DEGREE)


class FactTestCase(ModelTestCase):
    def test_fact_creation_successful(self):
        self.assertEqual(self.fact.title, self.F_TITLE)
        self.assertEqual(self.fact.content, self.F_CONTENT)


class HobbyTestCase(ModelTestCase):
    def test_hobby_creation_successful(self):
        self.assertEqual(self.hobby.name, self.H_NAME)


class JobTestCase(ModelTestCase):
    def test_job_creation_successful(self):
        self.assertEqual(self.job.company_name, self.J_COMPANY_NAME)
        self.assertEqual(self.job.position, self.J_POSITION)
        self.assertEqual(self.job.start_date, self.J_START_DATE)
        self.assertEqual(self.job.address, self.J_ADDRESS)
        self.assertEqual(self.job.job_type, self.J_JOB_TYPE)
        self.assertEqual(self.job.description, self.J_DESCRIPTION)


class LanguageTestCase(ModelTestCase):
    def test_language_creation_successful(self):
        self.assertEqual(self.language.name, self.L_NAME)
        self.assertEqual(self.language.level, self.L_LEVEL)


class ReferenceTestCase(ModelTestCase):
    def test_reference_creation_successful(self):
        self.assertEqual(self.reference.name, self.R_NAME)
        self.assertEqual(self.reference.profession, self.R_PROFESSION)
        self.assertEqual(self.reference.email, self.R_EMAIL)
        self.assertEqual(self.reference.phone, self.R_PHONE)
        self.assertEqual(self.reference.language, self.R_LANGUAGE)


class SocialMediaTestCase(ModelTestCase):
    def test_social_media_creation_successful(self):
        self.assertEqual(self.socialmedia.name, self.S_NAME)
        self.assertEqual(self.socialmedia.url, self.S_URL)
