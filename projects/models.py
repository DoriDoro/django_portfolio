from django.core.exceptions import ValidationError
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

# -- CONSTANT --
# -- Skill Choices --
CATEGORY_CHOICES = ["PROGRAMMING_SKILLS", "SOFT_SKILLS", "STRENGTH"]
SUBCATEGORY_CHOICES = ["BACKEND", "AUTH", "DATABASE", "DEV_OPS", "TOOLS"]


# -- Custom Manager --
class SkillDisplayActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True, display_skill=True)


# -- Model definition --
class Project(SlugCreateMixin, models.Model):
    """All Project details."""

    class TagChoices(models.TextChoices):
        OPENCLASSROOMS = "OPENCLASSROOMS", "openclassrooms"
        PERSONAL = "PERSONAL", "personal"

    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, blank=True, unique=True, editable=True)
    tag = models.CharField(max_length=16, choices=TagChoices.choices)
    legend = models.CharField(max_length=100)
    create_date = models.DateField()
    evaluation_date = models.DateField(null=True, blank=True)
    skill_set = HTMLField(validators=[validate_not_blank])
    introduction = HTMLField(validators=[validate_not_blank])
    experience = HTMLField(validators=[validate_not_blank])
    future = HTMLField(blank=True, null=True)
    picture = models.ImageField(
        upload_to=upload_to,
        storage=private_storage,
        validators=[validate_image_file],
        blank=True,
        null=True,
    )

    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    links = models.ManyToManyField("journal.Link", related_name="projects")
    skills = models.ManyToManyField("projects.Skill", related_name="projects")

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

    def clean(self):
        super().clean()
        if self.picture:
            img = Image.open(self.picture)
            if img.width < 800:
                raise ValidationError({"picture": "Image width must be at least 800 pixels."})
            self.picture.seek(0)

    def save(self, *args, **kwargs):
        clean = kwargs.pop("clean", True)
        update_fields = kwargs.get("update_fields")
        fields_to_update = set(update_fields) if update_fields is not None else None

        self._normalize_fields()

        if clean:
            self.full_clean()

        if self.pk:
            old_name = type(self).objects.filter(pk=self.pk).values_list("name", flat=True).first()
            if old_name != self.name:
                self.slug = ""
                if fields_to_update is not None:
                    fields_to_update.add("slug")

        if not self.slug:
            self.create_unique_slug(Project)
            if fields_to_update is not None:
                fields_to_update.add("slug")

        if fields_to_update is not None:
            kwargs["update_fields"] = list(fields_to_update)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("projects:portfolio-detail", kwargs={"slug": self.slug})


class Skill(models.Model):
    """Used stack."""

    class CategoryChoices(models.TextChoices):
        PROGRAMMING_SKILLS = "PROGRAMMING_SKILLS", _("Programming Skills")
        SOFT_SKILLS = "SOFT_SKILLS", _("Soft Skills")
        STRENGTH = "STRENGTH", _("Strength")

    class SubCategory(models.TextChoices):
        BACKEND = "BACKEND", _("Backend")
        AUTH = "AUTH", _("Authentication")
        DATABASE = "DATABASE", _("Database")
        DEV_OPS = "DEV_OPS", _("DevOps")
        TOOLS = "TOOLS", _("Tools")

    # general
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=18, choices=CategoryChoices.choices)
    # PROGRAMMING_SKILLS
    sub_category = models.CharField(
        max_length=8, choices=SubCategory.choices, blank=True, default=""
    )
    # STRENGTH
    content = models.CharField(max_length=500, blank=True, default="")

    display_skill = models.BooleanField(default=False)

    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active_skills = ActiveManager()
    display_active_skills = SkillDisplayActiveManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                "category",
                name="uq_skill_name_per_cat",
                violation_error_code="unique",
                violation_error_message="Skill name already exists for this category.",
            ),
            # include `sub_category=""` because a  sub_category can be "" by default
            models.CheckConstraint(
                condition=Q(category__in=CATEGORY_CHOICES),
                name="ck_skill_category",
                violation_error_code="check",
                violation_error_message="The category choice does not exist.",
            ),
            models.CheckConstraint(
                condition=Q(sub_category="") | Q(sub_category__in=SUBCATEGORY_CHOICES),
                name="ck_skill_sub_category",
                violation_error_code="check",
                violation_error_message="The sub_category choice does not exist.",
            ),
            models.CheckConstraint(
                condition=~Q(category="PROGRAMMING_SKILLS")
                | Q(sub_category__in=SUBCATEGORY_CHOICES),
                name="ck_skill_cat_sub_cat",
                violation_error_code="check",
                violation_error_message="Programming Skills require a sub category.",
            ),
            models.CheckConstraint(
                condition=~Q(category="STRENGTH") | ~Q(content=""),
                name="ck_skill_cat_soft_strength",
                violation_error_code="check",
                violation_error_message="Strength require 'content'.",
            ),
        ]
        indexes = [
            models.Index(fields=["display_skill", "active"], name="idx_display_skill_active"),
        ]
        ordering = [Lower("name"), "pk"]

    def __str__(self):
        return f"{self.name} ({self.category})"

    def _normalize_fields(self):
        if self.name:
            self.name = self.name.strip()
        if self.content:
            self.content = self.content.strip()

    def save(self, *args, **kwargs):
        clean = kwargs.pop("clean", True)
        self._normalize_fields()
        if clean:
            self.full_clean()
        return super().save(*args, **kwargs)
