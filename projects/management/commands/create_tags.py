from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction

from projects.models import Tag


class Command(BaseCommand):
    help = "This command creates all Job instances for DoriDoro."

    def handle(self, *args, **options):
        try:
            tags = [
                {
                    "name": "Python",
                    "category": Tag.PROGRAMMING_SKILLS,
                },
                {
                    "name": "Django",
                    "category": Tag.PROGRAMMING_SKILLS,
                },
                {
                    "name": "Django REST Framework",
                    "category": Tag.PROGRAMMING_SKILLS,
                },
                {
                    "name": "Flask",
                    "category": Tag.PROGRAMMING_SKILLS,
                },
                {
                    "name": "Unittest",
                    "category": Tag.PROGRAMMING_SKILLS,
                },
                {
                    "name": "Pytest",
                    "category": Tag.PROGRAMMING_SKILLS,
                },
                {
                    "name": "CLI application",
                    "category": Tag.PROGRAMMING_SKILLS,
                },
                {
                    "name": "Git",
                    "category": Tag.PROGRAMMING_SKILLS,
                },
                {
                    "name": "GitHub",
                    "category": Tag.PROGRAMMING_SKILLS,
                },
                {
                    "name": "GitHub actions",
                    "category": Tag.PROGRAMMING_SKILLS,
                },
                {
                    "name": "GitLab",
                    "category": Tag.PROGRAMMING_SKILLS,
                },
                {
                    "name": "Branching",
                    "category": Tag.PROGRAMMING_SKILLS,
                },
                {
                    "name": "SQLite",
                    "category": Tag.PROGRAMMING_SKILLS,
                },
                {
                    "name": "PostGreSQL",
                    "category": Tag.PROGRAMMING_SKILLS,
                },
                {
                    "name": "SQL",
                    "category": Tag.PROGRAMMING_SKILLS,
                },
                {
                    "name": "Postman",
                    "category": Tag.PROGRAMMING_SKILLS,
                },
                {
                    "name": "Celery",
                    "category": Tag.PROGRAMMING_SKILLS,
                },
                {
                    "name": "UML",
                    "category": Tag.PROGRAMMING_SKILLS,
                },
                {
                    "name": "Wireframe",
                    "category": Tag.PROGRAMMING_SKILLS,
                },
                {
                    "name": "User Story",
                    "category": Tag.PROGRAMMING_SKILLS,
                },
                {
                    "name": "ERD",
                    "category": Tag.PROGRAMMING_SKILLS,
                },
                {
                    "name": "Sentry",
                    "category": Tag.PROGRAMMING_SKILLS,
                },
                {
                    "name": "Docker",
                    "category": Tag.PROGRAMMING_SKILLS,
                },
                {
                    "name": "Heroku",
                    "category": Tag.PROGRAMMING_SKILLS,
                },
                {
                    "name": "Vercel",
                    "category": Tag.PROGRAMMING_SKILLS,
                },
                {
                    "name": "Render",
                    "category": Tag.PROGRAMMING_SKILLS,
                },
                {
                    "name": "Communication",
                    "category": Tag.SOFT_SKILLS,
                },
                {
                    "name": "Problem-solving",
                    "category": Tag.SOFT_SKILLS,
                },
                {
                    "name": "Attention to details",
                    "category": Tag.SOFT_SKILLS,
                },
                {
                    "name": "Time management",
                    "category": Tag.SOFT_SKILLS,
                },
                {
                    "name": "Continuous learning",
                    "category": Tag.SOFT_SKILLS,
                },
                {
                    "name": "Adaptability",
                    "category": Tag.SOFT_SKILLS,
                },
                {
                    "name": "Empathy",
                    "category": Tag.SOFT_SKILLS,
                },
                {
                    "name": "Positive attitude",
                    "category": Tag.SOFT_SKILLS,
                },
                {
                    "name": "Conflict resolution",
                    "category": Tag.SOFT_SKILLS,
                },
                {
                    "name": "Organisational ability with prioritisation",
                    "category": Tag.STRENGTH,
                },
                {
                    "name": "Quick comprehension",
                    "category": Tag.STRENGTH,
                },
                {
                    "name": "Independence",
                    "category": Tag.STRENGTH,
                },
                {
                    "name": "Personal responsibility",
                    "category": Tag.STRENGTH,
                },
                {
                    "name": "Reliable",
                    "category": Tag.STRENGTH,
                },
                {
                    "name": "Finish the job",
                    "category": Tag.STRENGTH,
                },
                {
                    "name": "Do not give up",
                    "category": Tag.STRENGTH,
                },
                {
                    "name": "Home office experience",
                    "category": Tag.STRENGTH,
                },
                {
                    "name": "Introverted",
                    "category": Tag.WEAKNESSES,
                },
                {
                    "name": "Shy",
                    "category": Tag.WEAKNESSES,
                },
                {
                    "name": "Make small talk",
                    "category": Tag.WEAKNESSES,
                },
                {
                    "name": "Perfectionism",
                    "category": Tag.WEAKNESSES,
                },
                {
                    "name": "Communication barrier in French",
                    "category": Tag.WEAKNESSES,
                },
                {
                    "name": "Afraid not to be good enough",
                    "category": Tag.WEAKNESSES,
                },
                {
                    "name": "PyCharm",
                    "category": Tag.OTHER,
                },
                {
                    "name": "Visual Studio Code",
                    "category": Tag.OTHER,
                },
                {
                    "name": "Linux (Ubuntu)",
                    "category": Tag.OTHER,
                },
                {
                    "name": "macOS",
                    "category": Tag.OTHER,
                },
            ]

            if Tag.objects.exists():
                self.stdout.write(
                    self.style.WARNING("These instances of Tag exists already!")
                )
                return

            with transaction.atomic():
                for tag in tags:
                    Tag.objects.create(**tag)

            self.stdout.write(
                self.style.SUCCESS("Instances of Tag successfully created!")
            )

        except IntegrityError:
            self.stdout.write(self.style.WARNING("These Tag instances exists already!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))
