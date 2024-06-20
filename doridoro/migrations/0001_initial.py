# Generated by Django 5.0.6 on 2024-06-20 20:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Achievement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        max_length=100, verbose_name="title of achievement"
                    ),
                ),
                ("content", models.TextField(verbose_name="content of achievement")),
                (
                    "published",
                    models.BooleanField(
                        default=True, verbose_name="achievement visible on website"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Degree",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "organization",
                    models.CharField(
                        max_length=100, verbose_name="organization of degree"
                    ),
                ),
                ("degree", models.CharField(max_length=100, verbose_name="degree")),
                (
                    "published",
                    models.BooleanField(
                        default=True, verbose_name="degree visible on website"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Fact",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=100, verbose_name="title of fact"),
                ),
                ("content", models.TextField(verbose_name="content of fact")),
                (
                    "published",
                    models.BooleanField(
                        default=True, verbose_name="fact visible on website"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Hobby",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=100, verbose_name="name of hobby"),
                ),
                (
                    "published",
                    models.BooleanField(
                        default=True, verbose_name="hobby visible on website"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "hobbies",
            },
        ),
        migrations.CreateModel(
            name="Job",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "company_name",
                    models.CharField(
                        max_length=200, verbose_name="company name of the job"
                    ),
                ),
                (
                    "position",
                    models.CharField(
                        max_length=200, verbose_name="position of the job"
                    ),
                ),
                ("start_date", models.DateField(verbose_name="start date of the job")),
                (
                    "end_date",
                    models.DateField(
                        blank=True, null=True, verbose_name="end date of the job"
                    ),
                ),
                (
                    "until_present",
                    models.BooleanField(default=False, verbose_name="until present"),
                ),
                (
                    "address",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="address of job",
                    ),
                ),
                (
                    "job_type",
                    models.CharField(
                        choices=[
                            ("FREELANCE", "Freelance"),
                            ("EMPLOYED", "Employed"),
                            ("APPRENTICESHIP", "Apprenticeship"),
                            ("FORMATION", "Formation"),
                            ("MENTORING", "MENTORING"),
                            ("PARENTAL_LEAVE", "Parental_Leave"),
                            ("SABBATICAL", "Sabbatical"),
                        ],
                        max_length=14,
                        verbose_name="type of job",
                    ),
                ),
                ("description", models.TextField(verbose_name="description of job")),
                (
                    "published",
                    models.BooleanField(
                        default=True, verbose_name="job visible on website"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Language",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="language")),
                (
                    "level",
                    models.CharField(
                        choices=[
                            ("A1", "A1 (Beginner)"),
                            ("A2", "A2 (Elementary)"),
                            ("B1", "B1 (Intermediate)"),
                            ("B2", "B2 (Upper Intermediate)"),
                            ("C1", "C1 (Advanced)"),
                            ("C2", "C2 (Proficient)"),
                            ("Native", "Native Speaker"),
                        ],
                        default="A1",
                        max_length=7,
                        verbose_name="level of language",
                    ),
                ),
                (
                    "published",
                    models.BooleanField(
                        default=True, verbose_name="language visible on website"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Reference",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=150, verbose_name="name of reference"),
                ),
                (
                    "profession",
                    models.CharField(
                        max_length=250, verbose_name="profession of reference"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=250, verbose_name="email address of reference"
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        blank=True, max_length=14, verbose_name="phone of reference"
                    ),
                ),
                (
                    "language",
                    models.CharField(
                        max_length=100, verbose_name="spoken language of reference"
                    ),
                ),
                (
                    "published",
                    models.BooleanField(
                        default=True, verbose_name="reference visible on website"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SocialMedia",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=150, verbose_name="name of social media"
                    ),
                ),
                (
                    "url",
                    models.URLField(max_length=250, verbose_name="url of social media"),
                ),
                (
                    "published",
                    models.BooleanField(
                        default=True, verbose_name="social media visible on website"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "SocialMedia",
            },
        ),
        migrations.CreateModel(
            name="Website",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=100, verbose_name="name of website"),
                ),
                ("url", models.URLField(max_length=250, verbose_name="url of website")),
                (
                    "published",
                    models.BooleanField(
                        default=True, verbose_name="url visible on website"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DoriDoro",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "phone",
                    models.CharField(max_length=14, verbose_name="phone of DoriDoro"),
                ),
                (
                    "address",
                    models.CharField(
                        max_length=150, verbose_name="address of DoriDoro"
                    ),
                ),
                (
                    "profession",
                    models.CharField(
                        max_length=150, verbose_name="profession of DoriDoro"
                    ),
                ),
                (
                    "introduction",
                    models.TextField(verbose_name="introduction of DoriDoro"),
                ),
                (
                    "dream_job",
                    models.TextField(verbose_name="dream job description of DoriDoro"),
                ),
                (
                    "free_time",
                    models.TextField(verbose_name="after work description of DoriDoro"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="doro_user",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user of DoriDoro",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "DoriDoro",
            },
        ),
    ]
