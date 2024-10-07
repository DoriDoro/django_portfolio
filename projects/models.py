from io import BytesIO

from django.core.files.base import ContentFile
from django.db import models
from django.utils.translation import gettext_lazy as _, gettext_lazy
from tinymce.models import HTMLField
from PIL import Image


class Project(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField()
    legend = models.CharField(max_length=100)
    create_date = models.DateField(verbose_name=_("create date"))
    evaluation_date = models.DateField(
        null=True, blank=True, verbose_name=_("evaluation date")
    )
    keywords = HTMLField()
    introduction = HTMLField()
    experience = HTMLField()
    future = HTMLField(null=True, blank=True)
    published = models.BooleanField(
        default=True, verbose_name=_("project visible on website")
    )
    links = models.ManyToManyField("Link", related_name="project_links")
    skills = models.ManyToManyField("Skill", related_name="project_skills")
    tags = models.ForeignKey(
        "Tag", on_delete=models.SET_NULL, null=True, related_name="project_tags"
    )
    doridoro = models.ForeignKey(
        "doridoro.DoriDoro",
        on_delete=models.SET_NULL,
        null=True,
        related_name="doro_project",
    )

    def __str__(self):
        return f"{self.title} ({self.published})"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.create_date = self.create_date
        else:
            old_instance = Project.objects.get(pk=self.pk)
            self.create_date = old_instance.create_date
        super().save(*args, **kwargs)


class Link(models.Model):
    class OriginChoices(models.TextChoices):
        GITHUB = "GITHUB", "GitHub"
        VERCEL = "VERCEL", "Vercel"
        RENDER = "RENDER", "Render"
        OTHER = "OTHER", _("Other")

    class PlatformChoices(models.TextChoices):
        OPENCLASSROOMS = "OPENCLASSROOMS", "OpenClasssrooms"
        PERSONAL_PROJECT = "PERSONAL_PROJECT", _("Personal Project")

    title = models.CharField(max_length=200)
    legend = models.CharField(max_length=100)
    origin = models.CharField(max_length=6, choices=OriginChoices)
    platform = models.CharField(max_length=17, choices=PlatformChoices)
    url = models.URLField()
    published = models.BooleanField(
        default=True, verbose_name=_("link visible on website")
    )

    def __str__(self):
        return self.url


class Picture(models.Model):
    legend = models.CharField(max_length=100)
    slug = models.SlugField()
    cover_picture = models.BooleanField(default=False, verbose_name=_("cover picture"))
    photo = models.ImageField(
        upload_to="images/",
        verbose_name=_("picture"),
        blank=True,
        null=True,
    )
    published = models.BooleanField(
        default=True, verbose_name=_("picture visible on website")
    )
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.SET_NULL,
        null=True,
        related_name="project_picture",
    )

    def __str__(self):
        return self.legend

    def save(self, *args, **kwargs):
        if self.photo:
            try:
                img = Image.open(self.photo)
                img.verify()
            except (IOError, SyntaxError) as e:
                raise ValueError(
                    gettext_lazy("The uploaded file is not a valid image. -- %s") % e
                )

            # Reopen the image to reset the file pointer
            try:
                img = Image.open(self.photo)
            except (IOError, SyntaxError) as e:
                raise ValueError(
                    gettext_lazy(
                        "The uploaded file could not be reopened as an image. -- %s"
                    )
                    % e
                )

            if img.width > 800:
                if img.mode in ("RGBA", "LA", "P"):
                    img = img.convert("RGB")

                # Calculate new dimensions to maintain aspect ratio with a width of 800
                new_width = 800
                original_width, original_height = img.size
                new_height = int((new_width / original_width) * original_height)

                try:
                    # Resize the image
                    img = img.resize((new_width, new_height), Image.LANCZOS)

                    # Save the image as JPEG
                    temp_img = BytesIO()
                    img.save(temp_img, format="JPEG", optimize=True)
                    temp_img.seek(0)

                    # Change file extension to .jpg
                    original_name, _ = self.photo.name.lower().split(".")
                    img_filename = f"{self.slug}.jpg"

                    # Save the BytesIO object to the ImageField with the new filename
                    self.photo.save(
                        img_filename, ContentFile(temp_img.read()), save=False
                    )
                except (IOError, SyntaxError) as e:
                    raise ValueError(
                        gettext_lazy(
                            "An error occurred while processing the image. -- %s"
                        )
                        % e
                    )

            else:
                raise ValueError(
                    gettext_lazy("The image width is smaller than 800 pixels.")
                )

        super().save(*args, **kwargs)


class Skill(models.Model):
    class SkillChoices(models.TextChoices):
        PROGRAMMING_SKILLS = "PROGRAMMING_SKILLS", _("Programming Skills")
        SOFT_SKILLS = "SOFT_SKILLS", _("Soft Skills")
        OTHER = "OTHER", _("Other")
        STRENGTH = "STRENGTH", _("Strength")
        WEAKNESSES = "WEAKNESSES", _("Weakness")

    name = models.CharField(max_length=50)
    category = models.CharField(max_length=20, choices=SkillChoices)
    published = models.BooleanField(
        default=True, verbose_name=_("skill visible on website")
    )

    def __str__(self):
        return f"{self.name} ({self.category})"


class Tag(models.Model):
    class TagChoices(models.TextChoices):
        OPENCLASSROOMS_PROJECT = "OPENCLASSROOMS_PROJECT", _("OpenClassrooms Project")
        PERSONAL_PROJECT = "PERSONAL_PROJECT", _("Personal Project")

    tag = models.CharField(max_length=22, choices=TagChoices)
    published = models.BooleanField(
        default=True, verbose_name=_("tag visible on website")
    )

    def __str__(self):
        return self.tag
