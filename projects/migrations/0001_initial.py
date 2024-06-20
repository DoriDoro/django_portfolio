# Generated by Django 5.0.6 on 2024-06-20 13:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("doridoro", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Link",
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
                ("url", models.URLField(verbose_name="url of link")),
                (
                    "published",
                    models.BooleanField(
                        default=True, verbose_name="link visible on website"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Tag",
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
                ("name", models.CharField(max_length=50, verbose_name="name of tag")),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("PROGRAMMING_SKILLS", "Programming Skills"),
                            ("SOFT_SKILLS", "Soft Skills"),
                            ("OTHER", "Other"),
                            ("STRENGTH", "Strength"),
                            ("WEAKNESSES", "Weakness"),
                        ],
                        max_length=20,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Project",
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
                    models.CharField(max_length=250, verbose_name="project title"),
                ),
                ("create_date", models.DateField(verbose_name="project created on")),
                ("introduction", models.TextField(verbose_name="project introduction")),
                ("content", models.TextField(verbose_name="project content")),
                (
                    "published",
                    models.BooleanField(
                        default=True, verbose_name="project visible on website"
                    ),
                ),
                (
                    "doridoro",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="doro_project",
                        to="doridoro.doridoro",
                        verbose_name="project of DoriDoro",
                    ),
                ),
                (
                    "links",
                    models.ManyToManyField(
                        related_name="project_links",
                        to="projects.link",
                        verbose_name="links of the project",
                    ),
                ),
                (
                    "tags",
                    models.ManyToManyField(
                        related_name="project_tags",
                        to="projects.tag",
                        verbose_name="tags of the project",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Image",
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
                    "legend",
                    models.CharField(max_length=100, verbose_name="legend of image"),
                ),
                (
                    "published",
                    models.BooleanField(
                        default=True, verbose_name="image visible on website"
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="project_image",
                        to="projects.project",
                        verbose_name="image of project",
                    ),
                ),
            ],
        ),
    ]
