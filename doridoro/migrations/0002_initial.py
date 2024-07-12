# Generated by Django 5.0.6 on 2024-07-12 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("doridoro", "0001_initial"),
        ("projects", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="job",
            name="links",
            field=models.ManyToManyField(
                related_name="job_links",
                to="projects.link",
                verbose_name="links of the job",
            ),
        ),
        migrations.AddField(
            model_name="job",
            name="tags",
            field=models.ManyToManyField(
                related_name="job_tags",
                to="projects.tag",
                verbose_name="tags of the job",
            ),
        ),
    ]
