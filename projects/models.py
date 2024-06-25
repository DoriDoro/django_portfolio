from io import BytesIO

from django.core.files.base import ContentFile
from django.db import models
from django.utils.translation import gettext_lazy as _
from PIL import Image


class Project(models.Model):
    title = models.CharField(max_length=250, verbose_name=_("project title"))
    create_date = models.DateField(verbose_name=_("project created on"))
    introduction = models.TextField(verbose_name=_("project introduction"))
    content = models.TextField(verbose_name=_("project content"))
    published = models.BooleanField(
        default=True, verbose_name=_("project visible on website")
    )
    tags = models.ManyToManyField(
        "Tag", related_name="project_tags", verbose_name=_("tags of the project")
    )
    links = models.ManyToManyField(
        "Link", related_name="project_links", verbose_name=_("links of the project")
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


class Picture(models.Model):
    legend = models.CharField(max_length=100, verbose_name=_("legend of image"))
    photo = models.ImageField(
        upload_to="portfolio/",
        verbose_name=_("photo"),
        blank=True,
        null=True,
    )
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

    def save(self, *args, **kwargs):
        if self.photo:
            try:
                img = Image.open(self.photo)
                img.verify()
                # reopen because img.verify() moves pointer to the end of the file
                img = Image.open(self.photo)

                # convert png to RGB
                if img.mode in ("RGBA", "LA", "P"):
                    img = img.convert("RGB")

                # Calculate new dimensions to maintain aspect ratio with a width of 800
                new_width = 800
                original_width, original_height = img.size
                new_height = int((new_width / original_width) * original_height)

                # Resize the image
                img = img.resize((new_width, new_height), Image.LANCZOS)

                # Prepare the image for saving
                temp_img = BytesIO()
                # Save the image as JPEG
                img.save(temp_img, format="JPEG", quality=70, optimize=True)
                temp_img.seek(0)

                # Change file extension to .jpg
                original_name, _ = self.photo.name.lower().split(".")
                img = f"{original_name}.jpg"

                # Save the BytesIO object to the ImageField with the new filename
                self.photo.save(img, ContentFile(temp_img.read()), save=False)

            except (IOError, SyntaxError) as e:
                raise ValueError(f"The uploaded file is not a valid image. -- {e}")

        super().save(*args, **kwargs)


class Link(models.Model):
    url = models.URLField(verbose_name=_("url of link"))
    published = models.BooleanField(
        default=True, verbose_name=_("link visible on website")
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
    name = models.CharField(max_length=50, verbose_name=_("name of tag/skill"))
    category = models.CharField(max_length=20, choices=TAG_CHOICES)
    published = models.BooleanField(
        default=True, verbose_name=_("tag/skill visible on website")
    )

    def __str__(self):
        return f"{self.name} ({self.category})"
