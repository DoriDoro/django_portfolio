from io import BytesIO

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import models
from django.db.models import Q
from django.db.models.functions import Lower
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField
from PIL import Image

from utils.database.images import upload_to, private_storage, validate_image_file
from utils.database.managers import ActiveManager
from utils.database.slug import SlugCreateMixin
from utils.database.validators import validate_not_blank


class Project(SlugCreateMixin, models.Model):
    """All Project details."""

    class TagChoices(models.TextChoices):
        OPENCLASSROOMS_PROJECT = "OPENCLASSROOMS_PROJECT", _("OpenClassrooms Project")
        PERSONAL_PROJECT = "PERSONAL_PROJECT", _("Personal Project")

    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, blank=True, unique=True, editable=True)
    tag = models.CharField(max_length=22, choices=TagChoices.choices)
    legend = models.CharField(max_length=100)
    create_date = models.DateField()
    evaluation_date = models.DateField(null=True, blank=True)
    skill_set = HTMLField(validators=[validate_not_blank])
    introduction = HTMLField(validators=[validate_not_blank])
    experience = HTMLField(validators=[validate_not_blank])
    future = HTMLField(blank=True, default="")

    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    links = models.ManyToManyField("projects.Link", related_name="projects")
    skills = models.ManyToManyField("projects.Skill", related_name="projects")
    doridoro = models.ForeignKey(
        "accounts.Profile",
        on_delete=models.SET_NULL,
        null=True,
        related_name="doro_projects",
    )

    objects = models.Manager()
    active_projects = ActiveManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                name="uq_project_name",
                violation_error_code="unique",
                violation_error_message="This project exists already.",
            )
        ]
        ordering = [Lower("name"), "pk"]

    def __str__(self):
        return f"{self.name} ({self.active})"

    def _normalize_fields(self):
        if self.name:
            self.name = self.name.strip()

    def save(self, *args, **kwargs):
        clean = kwargs.pop("clean", True)
        update_fields = kwargs.get("update_fields")
        fields_to_update = set(update_fields) if update_fields is not None else None

        self._normalize_fields()

        if clean:
            self.full_clean()

        if self.pk:
            old_name = (
                type(self)
                .objects.filter(pk=self.pk)
                .values_list("name", flat=True)
                .first()
            )
            if old_name != self.name:
                self.slug = ""
                if fields_to_update is not None:
                    fields_to_update.add("slug")

        if not self.slug:
            self.create_unique_slug(Project)
            if fields_to_update is not None:
                fields_to_update.add("slug")

        if fields_to_update is not None:
            kwargs["update_fields"] = fields_to_update
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("projects:portfolio-detail", kwargs={"slug": self.slug})


class Link(models.Model):
    """Link for the project."""

    class OriginChoices(models.TextChoices):
        GITHUB = "GITHUB", "GitHub"
        VERCEL = "VERCEL", "Vercel"
        RENDER = "RENDER", "Render"
        OTHER = "OTHER", _("Other")

    class PlatformChoices(models.TextChoices):
        OPENCLASSROOMS = "OPENCLASSROOMS", "OpenClassrooms"
        PERSONAL_PROJECT = "PERSONAL_PROJECT", _("Personal Project")

    title = models.CharField(max_length=200)
    origin = models.CharField(max_length=6, choices=OriginChoices.choices)
    platform = models.CharField(max_length=16, choices=PlatformChoices)
    url = models.URLField()

    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active_links = ActiveManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("title"),
                name="uq_link_title",
                violation_error_code="unique",
                violation_error_message="This Link exists already.",
            )
        ]
        ordering = [Lower("title"), "pk"]

    def __str__(self):
        return self.title

    def _normalize_fields(self):
        if self.title:
            self.title = self.title.strip()
        if self.url:
            self.url = self.url.strip()

    def save(self, *args, **kwargs):
        clean = kwargs.pop("clean", True)
        self._normalize_fields()
        if clean:
            self.full_clean()
        super().save(*args, **kwargs)


class Picture(SlugCreateMixin, models.Model):
    """Images for the Project."""

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True, unique=True, editable=True)
    picture = models.ImageField(
        upload_to=upload_to,
        storage=private_storage,
        validators=[validate_image_file],
        blank=True,
        null=True,
    )
    cover_picture = models.BooleanField(default=False)

    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.SET_NULL,
        null=True,
        related_name="pictures",
    )

    objects = models.Manager()
    active_pictures = ActiveManager()

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(cover_picture=False) | Q(project__isnull=False),
                name="ck_pic_cover_req_project",
                violation_error_code="check",
                violation_error_message="This cover picture has to be connected to a Project.",
            ),
            models.UniqueConstraint(
                fields=["project"],
                condition=Q(cover_picture=True, active=True, project__isnull=False),
                name="uq_pic_one_active_cover_per_project",
                violation_error_code="unique",
                violation_error_message="One cover picture needed for an active project.",
            ),
        ]
        ordering = [Lower("title"), "pk"]

    def __str__(self):
        return self.title

    def _normalize_fields(self):
        if self.title:
            self.title = self.title.strip()

    def _process_image(self):
        if not self.picture:
            return
        img = Image.open(self.picture)
        if img.width <= 800:
            raise ValidationError(
                {"picture": "Image width must be at least 800 pixels."}
            )
        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGB")
        new_height = int((800 / img.width) * img.height)
        try:
            img = img.resize((800, new_height), Image.LANCZOS)
            temp_img = BytesIO()
            img.save(temp_img, format="JPEG", optimize=True)
            temp_img.seek(0)
            self.picture.save(
                f"{self.slug}.jpg", ContentFile(temp_img.read()), save=False
            )
        except (IOError, SyntaxError) as e:
            raise ValidationError({"picture": f"Image processing failed: {e}"})

    def save(self, *args, **kwargs):
        clean = kwargs.pop("clean", True)
        update_fields = kwargs.get("update_fields")
        fields_to_update = set(update_fields) if update_fields is not None else None
        self._normalize_fields()
        if clean:
            self.full_clean()

        if self.pk:
            old_title = (
                type(self)
                .objects.filter(pk=self.pk)
                .values_list("title", flat=True)
                .first()
            )
            if old_title != self.title:
                self.slug = ""
                if fields_to_update is not None:
                    fields_to_update.add("title")

        if not self.slug:
            self.create_unique_slug(Picture, field_name="title")
            if fields_to_update is not None:
                fields_to_update.add("slug")

        self._process_image()

        if fields_to_update is not None:
            kwargs["update_fields"] = fields_to_update
        super().save(*args, **kwargs)


class Skill(models.Model):
    """Used stack."""

    class SkillChoices(models.TextChoices):
        PROGRAMMING_SKILLS = "PROGRAMMING_SKILLS", _("Programming Skills")
        SOFT_SKILLS = "SOFT_SKILLS", _("Soft Skills")
        OTHER = "OTHER", _("Other")
        STRENGTH = "STRENGTH", _("Strength")
        WEAKNESSES = "WEAKNESSES", _("Weakness")

    name = models.CharField(max_length=50)
    category = models.CharField(max_length=18, choices=SkillChoices.choices)

    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active_skills = ActiveManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                "category",
                name="uq_skill_name_category",
                violation_error_code="unique",
                violation_error_message="This name-category-combination exists already.",
            ),
        ]
        ordering = [Lower("name"), "pk"]

    def __str__(self):
        return f"{self.name} ({self.category})"

    def _normalize_fields(self):
        if self.name:
            self.name = self.name.strip()

    def save(self, *args, **kwargs):
        clean = kwargs.pop("clean", True)
        self._normalize_fields()
        if clean:
            self.full_clean()
        return super().save(*args, **kwargs)
