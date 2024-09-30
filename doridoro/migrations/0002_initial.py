# Generated by Django 5.0.6 on 2024-09-28 08:07

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
            field=models.ManyToManyField(related_name="job_links", to="projects.link"),
        ),
        migrations.AddField(
            model_name="job",
            name="skill",
            field=models.ManyToManyField(
                related_name="job_skills", to="projects.skill"
            ),
        ),
    ]
