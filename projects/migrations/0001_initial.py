# Generated by Django 5.0.6 on 2024-07-13 11:56

import django.db.models.deletion
import tinymce.models
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
                (
                    "title",
                    models.CharField(max_length=200, verbose_name="title of link"),
                ),
                (
                    "legend",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="legend of link",
                    ),
                ),
                (
                    "origin",
                    models.CharField(
                        choices=[
                            ("GITHUB", "GitHub"),
                            ("VERCEL", "Vercel"),
                            ("OTHER", "Other"),
                        ],
                        max_length=6,
                        verbose_name="origin of link",
                    ),
                ),
                (
                    "platform",
                    models.CharField(
                        choices=[
                            ("OPENCLASSROOMS", "OpenClasssrooms"),
                            ("PERSONAL_PROJECT", "Personal Project"),
                        ],
                        max_length=17,
                        verbose_name="platform of link",
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
                (
                    "name",
                    models.CharField(max_length=50, verbose_name="name of tag/skill"),
                ),
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
                        verbose_name="category of tag/skill",
                    ),
                ),
                (
                    "published",
                    models.BooleanField(
                        default=True, verbose_name="tag/skill visible on website"
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
                ("slug", models.SlugField(verbose_name="project slug")),
                ("create_date", models.DateField(verbose_name="project created on")),
                (
                    "introduction",
                    tinymce.models.HTMLField(verbose_name="project introduction"),
                ),
                ("content", tinymce.models.HTMLField(verbose_name="project content")),
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
            name="Picture",
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
                    models.CharField(max_length=100, verbose_name="legend of picture"),
                ),
                ("slug", models.SlugField(verbose_name="slug of picture")),
                (
                    "cover_picture",
                    models.BooleanField(default=False, verbose_name="cover picture"),
                ),
                (
                    "photo",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="images/",
                        verbose_name="picture",
                    ),
                ),
                (
                    "published",
                    models.BooleanField(
                        default=True, verbose_name="picture visible on website"
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="project_picture",
                        to="projects.project",
                        verbose_name="picture of project",
                    ),
                ),
            ],
        ),
    ]
