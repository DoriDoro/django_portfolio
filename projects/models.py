from django.db import models
from django.utils.translation import gettext_lazy as _


class Project(models.Model):
    title = models.CharField(max_length=250, verbose_name=_("project title"))
    create_date = models.DateField(verbose_name=_("project created on"))
    introduction = models.TextField(verbose_name=_("project introduction"))
    content = models.TextField(verbose_name=_("project content"))
    published = models.BooleanField(
        default=True, verbose_name=_("project visible on website")
    )
    tags = models.ManyToManyField(
        "Tag", related_name="project_tag", verbose_name=_("tags of the project")
    )
    doridoro = models.ForeignKey(
        "doridoro.DoriDoro",
        on_delete=models.SET_NULL,
        null=True,
        related_name="doro_project",
        verbose_name=_("project of DoriDoro"),
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            self.create_date = self.create_date
        else:
            old_instance = Project.object.get(pk=self.pk)
            self.create_date = old_instance.create_date
        super().save(*args, **kwargs)


class Image(models.Model):
    legend = models.CharField(max_length=100, verbose_name=_("legend of image"))
    # photo = models.ImageField(
    #     upload_to="images", verbose_name=_("image"), blank=True, null=True
    # )
    published = models.BooleanField(
        default=True, verbose_name=_("image visible on website")
    )
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="project_image",
        verbose_name=_("image of project"),
    )

    def __str__(self):
        return self.legend


class Link(models.Model):
    url = models.URLField(verbose_name=_("url of link"))
    published = models.BooleanField(
        default=True, verbose_name=_("link visible on website")
    )
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="project_link",
        verbose_name=_("link of project"),
    )

    def __str__(self):
        return self.url


class Tag(models.Model):
    # tag is a skill
    PROGRAMMING_SKILLS = "PROGRAMMING_SKILLS"
    SOFT_SKILLS = "SOFT_SKILLS"
    OTHER = "OTHER"
    STRENGTH = "STRENGTH"
    WEAKNESSES = "WEAKNESSES"

    TAG_CHOICES = [
        (PROGRAMMING_SKILLS, _("Programming Skills")),
        (SOFT_SKILLS, _("Soft Skills")),
        (OTHER, _("Other")),
        (STRENGTH, _("Strength")),
        (WEAKNESSES, _("Weakness")),
    ]
    name = models.CharField(max_length=50, verbose_name=_("name of tag"))
    category = models.CharField(max_length=20, choices=TAG_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.category})"
