from io import BytesIO

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import models
from django.db.models import Q, F
from django.db.models.functions import Lower
from django.urls import reverse
from django.utils.translation import gettext_lazy as _, gettext_lazy
from tinymce.models import HTMLField
from typing import Dict
from PIL import Image

from utils.manager.managers import ActiveManager
from utils.slug.mixins import SlugCreateMixin


class Project(SlugCreateMixin, models.Model):
    """All Project details."""

    title = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=250, blank=True, unique=True, editable=True)
    legend = models.CharField(max_length=100)
    create_date = models.DateField()
    evaluation_date = models.DateField(null=True, blank=True)
    keywords = HTMLField(verbose_name=_("skill set of project"))
    introduction = HTMLField()
    experience = HTMLField()
    future = HTMLField(null=True, blank=True, verbose_name=_("future plans of project"))

    active = models.BooleanField(
        default=True, verbose_name=_("project visible on website"), db_index=True
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    links = models.ManyToManyField("Link", related_name="project_links")
    skills = models.ManyToManyField("Skill", related_name="project_skills")
    tags = models.ForeignKey(
        "Tag",
        on_delete=models.SET_NULL,
        null=True,
        related_name="project_tags",
    )
    doridoro = models.ForeignKey(
        "doridoro.DoriDoro",
        on_delete=models.SET_NULL,
        null=True,
        related_name="doro_project",
    )

    objects = models.Manager()
    active_projects = ActiveManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("title"),
                condition=Q(active=True),
                name="uix_project_low_title_active",
            ),
            # evaluation_date must be >= create_date (or null)
            models.CheckConstraint(
                check=Q(evaluation_date__gte=F("create_date"))
                | Q(evaluation_date__isnull=True),
                name="ck_project_eval_creation",
            ),
        ]
        indexes = [
            # Common: active list ordered by newest
            models.Index(fields=["-created"], name="idx_project_created_desc"),
            models.Index(
                fields=["active", "-created"], name="idx_project_active_created"
            ),
            # Useful if you filter by these a lot
            models.Index(fields=["tags", "active"], name="idx_project_tag_active"),
            models.Index(
                fields=["doridoro", "active"], name="idx_project_doridoro_active"
            ),
        ]
        ordering = ["-created"]

    def __str__(self):
        return f"{self.title} ({self.active})"

    def get_absolute_url(self):
        return reverse("projects:portfolio-detail", kwargs={"slug": self.slug})

    def clean(self):
        errors: Dict[str, str] = {}

        if self.title:
            self.title = self.title.strip()

        if (
            self.title
            and Project.objects.filter(name__iexact=self.title)
            .exclude(pk=self.pk)
            .exists()
        ):
            errors["title"] = f"Project with name: '{self.title}' exists already."

        if (
            self.evaluation_date
            and self.create_date
            and self.evaluation_date < self.create_date
        ):
            errors["evaluation_date"] = (
                "Evaluation date cannot be before creation date."
            )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        if self.title:
            self.title = self.title.strip()

        if not self.slug and self.title:
            self.create_unique_slug(Project, field_name="title")
        self.full_clean()
        super().save(*args, **kwargs)


class Link(models.Model):
    """Link for the project."""

    class OriginChoices(models.TextChoices):
        GITHUB = "GITHUB", "GitHub"
        VERCEL = "VERCEL", "Vercel"
        RENDER = "RENDER", "Render"
        OTHER = "OTHER", _("Other")

    class PlatformChoices(models.TextChoices):
        OPENCLASSROOMS = "OPENCLASSROOMS", "OpenClasssrooms"
        PERSONAL_PROJECT = "PERSONAL_PROJECT", _("Personal Project")

    title = models.CharField(max_length=200, db_index=True)
    legend = models.CharField(max_length=100)
    origin = models.CharField(max_length=6, choices=OriginChoices, db_index=True)
    platform = models.CharField(max_length=16, choices=PlatformChoices, db_index=True)
    url = models.URLField()

    active = models.BooleanField(
        default=True, verbose_name=_("link visible on website"), db_index=True
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            # Case-insensitive unique title for active=True
            models.UniqueConstraint(
                Lower("title"),
                condition=Q(active=True),
                name="uix_link_low_title_active",
            ),
            # Avoid duplicate Links with same url and origin for active=True
            models.UniqueConstraint(
                fields=["url", "origin"],
                condition=Q(active=True),
                name="uix_link_url_origin",
            ),
        ]
        indexes = [
            # Common: filter active links and list/sort by title
            models.Index(fields=["active", "title"], name="idx_link_active_title"),
            models.Index(fields=["active", "origin"], name="idx_link_active_origin"),
            models.Index(
                fields=["active", "platform"], name="idx_link_active_platform"
            ),
        ]
        ordering = ["title", "pk"]

    def __str__(self):
        return self.title

    def clean(self):
        errors: Dict[str, str] = {}

        # Normalize
        if self.title:
            self.title = self.title.strip()
        if self.legend:
            self.legend = self.legend.strip()
        if self.url:
            self.url = self.url.strip()

        if self.url and self.origin:
            qs = Link.objects.filter(url=self.url, origin=self.origin)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                errors["url"] = "A link with this URL and origin already exists."

        # If you want title to be required meaningfully (not just whitespace)
        if self.title is not None and not self.title.strip():
            errors["title"] = "Title cannot be empty."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Picture(SlugCreateMixin, models.Model):
    """Images for the Project."""

    legend = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=250, blank=True, unique=True, editable=True)
    photo = models.ImageField(
        upload_to="images/",
        verbose_name=_("picture"),
        blank=True,
        null=True,
    )
    cover_picture = models.BooleanField(default=False)

    active = models.BooleanField(
        default=True, verbose_name=_("picture visible on website"), db_index=True
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.SET_NULL,
        null=True,
        related_name="pictures",
    )

    def __str__(self):
        return self.legend

    class Meta:
        constraints = [
            # If it's marked as cover, it must belong to a project (avoids project=NULL cover rows)
            models.CheckConstraint(
                check=Q(cover_picture=False) | Q(project__isnull=False),
                name="picture_cover_requires_project",
            ),
            # At most one ACTIVE cover picture per project
            models.UniqueConstraint(
                fields=["project"],
                condition=Q(cover_picture=True, active=True, project__isnull=False),
                name="uix_picture_one_active_cover_per_project",
            ),
        ]
        indexes = [
            models.Index(
                fields=["project", "active"], name="idx_picture_project_active"
            ),
            models.Index(
                fields=["project", "cover_picture"], name="idx_picture_project_cover"
            ),
            models.Index(
                fields=["active", "-created"], name="idx_picture_active_created"
            ),
        ]
        ordering = ["legend", "pk"]

    def clean(self):
        errors: Dict[str, str] = {}

        # Normalize
        if self.legend:
            self.legend = self.legend.strip()

        # Make sure legend is not only whitespace
        if self.legend is not None and not self.legend.strip():
            errors["legend"] = "Legend cannot be empty or a whitespace."

        # Validate the cover picture is attached to a project
        if self.cover_picture and self.project is None:
            errors["project"] = "A cover picture must be attached to a project."

        # Cover picture has to be active:
        if self.cover_picture and not self.active:
            errors["active"] = "A cover picture must be active."

        if errors:
            raise ValidationError(errors)

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

        if self.legend:
            self.legend = self.legend.strip()

        if not self.slug and self.legend:
            self.create_unique_slug(Picture, field_name="legend")

        self.full_clean()
        super().save(*args, **kwargs)


class Skill(models.Model):
    """Used stack."""

    class SkillChoices(models.TextChoices):
        PROGRAMMING_SKILLS = "PROGRAMMING_SKILLS", _("Programming Skills")
        SOFT_SKILLS = "SOFT_SKILLS", _("Soft Skills")
        OTHER = "OTHER", _("Other")
        STRENGTH = "STRENGTH", _("Strength")
        WEAKNESSES = "WEAKNESSES", _("Weakness")

    name = models.CharField(max_length=50, db_index=True)
    category = models.CharField(max_length=18, choices=SkillChoices)

    active = models.BooleanField(
        default=True, verbose_name=_("skill visible on website"), db_index=True
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                "category",
                condition=Q(active=True),
                name="uix_skill_name_category_active",
            ),
        ]
        indexes = [
            models.Index(
                fields=["active", "category", "name"], name="idx_skill_active_cat_name"
            ),
            models.Index(
                fields=["category", "active"], name="idx_skill_category_active"
            ),
        ]
        ordering = [Lower("name"), "pk"]

    def __str__(self):
        return f"{self.name} ({self.category})"

    def clean(self):
        errors: Dict[str, str] = {}

        if self.name:
            # Normalize whitespace
            self.name = " ".join(self.name.strip().split())

        if self.name is not None and not self.name:
            errors["name"] = "Skill name cannot be empty."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Tag(models.Model):
    """Group Projects for personal projects or projects of OpenClassrooms."""

    class TagChoices(models.TextChoices):
        OPENCLASSROOMS_PROJECT = "OPENCLASSROOMS_PROJECT", _("OpenClassrooms Project")
        PERSONAL_PROJECT = "PERSONAL_PROJECT", _("Personal Project")

    tag = models.CharField(max_length=22, choices=TagChoices, db_index=True)

    active = models.BooleanField(
        default=True, verbose_name=_("tag visible on website"), db_index=True
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["tag"],
                name="uix_tag_unique_tag",
            ),
        ]
        indexes = [
            models.Index(fields=["tag", "active"], name="idx_tag_active"),
        ]
        ordering = ["tag", "pk"]

    def __str__(self):
        return self.get_tag_display()

    def clean(self):
        super().clean()
        errors: Dict[str, str] = {}

        if not self.tag:
            errors["tag"] = "Tag value is required."

        # Prevent changing the tag once created
        if self.pk:
            original = (
                Tag.objects.filter(pk=self.pk).values_list("tag", flat=True).first()
            )
            if original and original != self.tag:
                errors["tag"] = "Tag value cannot be modified once created."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
