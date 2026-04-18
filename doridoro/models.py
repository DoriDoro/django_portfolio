from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField
from typing import Dict

from utils.manager.managers import ActiveManager
from utils.database.validators import validate_not_blank

# --- CONSTANTS: Language model ---
LANGUAGE_CHOICES = ["A1", "A2", "B1", "B2", "C1", "C2", "Native"]


class DoriDoro(models.Model):
    """Instance of myself, to represent details."""

    phone = models.CharField(max_length=14)
    address = models.CharField(max_length=150)

    profession = models.CharField(max_length=150)
    introduction = HTMLField()
    dream_job = HTMLField(verbose_name=_("dream job description"))
    free_time = HTMLField(verbose_name=_("after work description"))

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    user = models.OneToOneField(
        "accounts.User",
        null=True,
        on_delete=models.SET_NULL,
        related_name="doro_user",
        verbose_name=_("user instance"),
    )

    class Meta:
        verbose_name_plural = "DoriDoro"

    def __str__(self):
        return self.get_full_name

    @property
    def get_full_name(self):
        if self.user:
            return f"{self.user.first_name} {self.user.last_name}"
        return ""


class Achievement(models.Model):
    """Challenges and Milestones."""

    title = models.CharField(max_length=300, db_index=True)
    content = models.TextField(validators=[validate_not_blank])

    active = models.BooleanField(
        default=True, verbose_name=_("achievement visible on website"), db_index=True
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # --- Managers ---
    objects = models.Manager()
    active_achievements = ActiveManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("title"),
                name="uix_achieve_low_title",
            )
        ]
        indexes = [
            models.Index(fields=["title", "active"], name="idx_achieve_title_active")
        ]
        ordering = ["title", "pk"]

    def __str__(self):
        return f"{self.title} ({self.active})"

    def clean(self):
        errors: Dict[str, str] = {}

        if self.title:
            self.title = self.title.strip()

        if (
            self.title
            and Achievement.objects.filter(title__iexact=self.title)
            .exclude(pk=self.pk)
            .exists()
        ):
            errors["title"] = f"Achievement exists with title: '{self.title}'."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Degree(models.Model):
    """Reached degrees."""

    organization = models.CharField(max_length=100, db_index=True)
    degree = models.CharField(max_length=100)
    url = models.URLField(max_length=250, null=True, blank=True)

    active = models.BooleanField(
        default=True, verbose_name=_("degree visible on website"), db_index=True
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active_degrees = ActiveManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("organization"),
                Lower("degree"),
                name="uix_degree_low_orga_degree",
            ),
        ]
        indexes = [
            models.Index(
                fields=["organization", "active"], name="idx_degree_orga_active"
            ),
            models.Index(fields=["degree", "active"], name="idx_degree_degree_active"),
        ]
        ordering = ["organization", "pk"]

    def __str__(self):
        return f"{self.organization} ({self.active})"

    def clean(self):
        errors: Dict[str, str] = {}

        if self.organization:
            self.organization = self.organization.strip()

        if self.degree:
            self.degree = self.degree.strip()

        if (
            self.organization
            and self.degree
            and Degree.objects.filter(
                organization__iexact=self.organization, degree__iexact=self.degree
            )
            .exclude(pk=self.pk)
            .exists()
        ):
            errors["organization"] = (
                f"Degree with organisation name and degree title: '{self.organization}' exists already."
            )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Fact(models.Model):
    """Short details to inform."""

    title = models.CharField(max_length=100, db_index=True)
    content = models.TextField(validators=[validate_not_blank])

    active = models.BooleanField(
        default=True, verbose_name=_("fact visible on website"), db_index=True
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active_facts = ActiveManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("title"),
                "content",
                name="uix_fact_title_content",
            )
        ]
        indexes = [
            models.Index(fields=["title", "active"], name="idx_fact_title_active")
        ]
        ordering = ["title", "pk"]

    def __str__(self):
        return f"{self.title} ({self.active})"

    def clean(self):
        errors: Dict[str, str] = {}

        if self.title:
            self.title = self.title.strip()

        if (
            self.title
            and Fact.objects.filter(title__iexact=self.title, content=self.content)
            .exclude(pk=self.pk)
            .exists()
        ):
            errors["title"] = "Fact with this title and content exists already."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Hobby(models.Model):
    """Interests."""

    name = models.CharField(max_length=100, db_index=True)

    active = models.BooleanField(
        default=True, verbose_name=_("hobby visible on website"), db_index=True
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active_hobbies = ActiveManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(Lower("name"), name="uix_hobby_low_name")
        ]
        indexes = [
            models.Index(fields=["name", "active"], name="idx_hobby_name_active")
        ]
        ordering = ["name", "pk"]
        verbose_name_plural = "Hobbies"

    def __str__(self):
        return f"{self.name} ({self.active})"

    def clean(self):
        errors: Dict[str, str] = {}

        if self.name:
            self.name = self.name.strip()

        if (
            self.name
            and Hobby.objects.filter(name__iexact=self.name)
            .exclude(pk=self.pk)
            .exists()
        ):
            errors["name"] = f"Hobby with name: '{self.name}' exists already."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Job(models.Model):
    """All jobs."""

    class JobType(models.TextChoices):
        FREELANCE = "FREELANCE", _("Freelance")
        EMPLOYED = "EMPLOYED", _("Employed")
        APPRENTICESHIP = "APPRENTICESHIP", _("Apprenticeship")
        FORMATION = "FORMATION", _("Formation")
        MENTORING = "MENTORING", _("Mentoring")
        PARENTAL_LEAVE = "PARENTAL_LEAVE", _("Parental_Leave")
        SABBATICAL = "SABBATICAL", _("Sabbatical")

    company_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
    )
    address = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=200, db_index=True)
    description = models.TextField(validators=[validate_not_blank])
    job_type = models.CharField(
        max_length=14, choices=JobType, verbose_name=_("job type")
    )

    start_date = models.DateField(verbose_name=_("start date"))
    end_date = models.DateField(blank=True, null=True, verbose_name=_("end date"))
    until_present = models.BooleanField(default=False, verbose_name=_("present"))

    active = models.BooleanField(
        default=True, verbose_name=_("job visible on website"), db_index=True
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    skill = models.ManyToManyField("projects.Skill", related_name="job_skills")
    links = models.ManyToManyField("projects.Link", related_name="job_links")

    objects = models.Manager()
    active_jobs = ActiveManager()

    class Meta:
        constraints = [
            # Uniqueness: same position, company & start_date should not be duplicated
            models.UniqueConstraint(
                Lower("position"),
                Lower("company_name"),
                "start_date",
                name="uix_job_position_company_start",
            ),
            # If until_present is True, end_date must be NULL
            models.CheckConstraint(
                check=~Q(until_present=True) | Q(end_date__isnull=True),
                name="ch_job_present_no_end",
            ),
            # end_date must be >= start_date or NULL
            models.CheckConstraint(
                check=Q(end_date__gte=F("start_date")) | Q(end_date__isnull=True),
                name="ch_job_start_before_end",
            ),
        ]
        indexes = [
            models.Index(
                fields=["position", "job_type", "active"],
                name="idx_job_pos_type_active",
            ),
            models.Index(fields=["-start_date", "-end_date"], name="idx_job_dates"),
        ]
        ordering = ["position", "pk"]

    def __str__(self):
        return f"{self.job_type} ({self.company_name} - {self.active})"

    def clean(self):
        errors: Dict[str, str] = {}

        # Normalize strings
        if self.position:
            self.position = self.position.strip()
        if self.company_name:
            self.company_name = self.company_name.strip()
        if self.address:
            self.address = self.address.strip()

        # Logical checks: until_present / end_date
        if self.until_present and self.end_date is not None:
            errors["until_present"] = (
                "If the job is ongoing, the end date should be empty."
            )

        if not self.until_present and self.end_date is None:
            errors["end_date"] = "End date must be provided if the job is not ongoing."

        if self.end_date and self.start_date and self.end_date < self.start_date:
            errors["end_date"] = "End date should be after start date."

        # Position cannot be blank/whitespace
        if not (self.position and self.position.strip()):
            errors["position"] = "Position can not be blank or only space."

        # Company required for certain job types
        if self.job_type in [
            self.JobType.EMPLOYED,
            self.JobType.APPRENTICESHIP,
            self.JobType.FORMATION,
        ] and not (self.company_name and self.company_name.strip()):
            errors["company_name"] = (
                "Company name is required for job types: "
                "Employed, Apprenticeship or Formation."
            )

        # Optional: enforce the same uniqueness at the application level
        if self.position and self.start_date:
            qs = Job.objects.filter(
                position__iexact=self.position,
                start_date=self.start_date,
                company_name__iexact=self.company_name or "",
            )
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                errors["position"] = (
                    "Job with this position, company and start date already exists."
                )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Language(models.Model):
    """Spoken languages."""

    class LevelChoices(models.TextChoices):
        A1 = "A1", _("A1 - Beginner")
        A2 = "A2", _("A2 - Elementary")
        B1 = "B1", _("B1 - Intermediate")
        B2 = "B2", _("B2 - Upper Intermediate")
        C1 = "C1", _("C1 - Advanced")
        C2 = "C2", _("C2 - Proficient")
        NATIVE = "Native", _("Native Speaker")

    name = models.CharField(max_length=50, db_index=True)
    level = models.CharField(
        max_length=6,
        choices=LevelChoices,
        default=LevelChoices.A1,
    )

    active = models.BooleanField(
        default=True, verbose_name=_("language visible on website"), db_index=True
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active_languages = ActiveManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(Lower("name"), name="uix_lang_low_name"),
            # DB-level guarantee matching LANGUAGE_CHOICES
            models.CheckConstraint(
                name="ck_lang_level_valid",
                check=Q(level__in=[l for l in LANGUAGE_CHOICES]),
            ),
        ]
        indexes = [models.Index(Lower("name"), "active", name="idx_lang_name_active")]
        ordering = ["name", "pk"]

    def __str__(self):
        return f"{self.name} ({self.level} - {self.active})"

    def clean(self):
        errors: Dict[str, str] = {}

        if self.name:
            self.name = self.name.strip()

        if (
            self.name
            and Language.objects.filter(name__iexact=self.name)
            .exclude(pk=self.pk)
            .exists()
        ):
            errors["name"] = f"Language '{self.name}' already exists."

        if self.level and self.level not in LANGUAGE_CHOICES:
            errors["level"] = "Invalid language level."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Reference(models.Model):
    """Contact details for references."""

    name = models.CharField(max_length=150, db_index=True)
    profession = models.CharField(max_length=250)
    email = models.EmailField(
        blank=True, null=True, max_length=250, verbose_name=_("email address")
    )
    phone = models.CharField(blank=True, null=True, max_length=14)

    language = models.CharField(max_length=100, verbose_name=_("spoken language"))

    active = models.BooleanField(
        default=True, verbose_name=_("reference visible on website"), db_index=True
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active_references = ActiveManager()

    class Meta:
        constraints = [models.UniqueConstraint(Lower("name"), name="uix_ref_low_name")]
        indexes = [models.Index(fields=["name", "active"], name="idx_ref_name_active")]
        ordering = ["name", "pk"]

    def __str__(self):
        return f"{self.name} ({self.active})"

    def clean(self):
        errors: Dict[str, str] = {}

        if self.name:
            self.name = self.name.strip()
        if self.profession:
            self.profession = self.profession.strip()
        if self.language:
            self.language = self.language.strip()

        # At least one contact method
        if not (self.email or self.phone):
            errors["email"] = "Provide at least an email or a phone number."
            errors["phone"] = "Provide at least an email or a phone number."

        # Case-insensitive uniqueness on name
        if (
            self.name
            and Reference.objects.filter(name__iexact=self.name)
            .exclude(pk=self.pk)
            .exists()
        ):
            errors["name"] = f"Reference with name '{self.name}' already exists."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class SocialMedia(models.Model):
    """Links to my SocialMedia."""

    name = models.CharField(max_length=150, db_index=True)
    url = models.URLField(max_length=250, verbose_name=_("url of social media"))

    active = models.BooleanField(
        default=True, verbose_name=_("social media visible on website"), db_index=True
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active_social_medias = ActiveManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(Lower("name"), name="uix_social_media_low_name")
        ]
        indexes = [
            models.Index(fields=["name", "active"], name="idx_social_media_name_active")
        ]
        ordering = ["name", "pk"]
        verbose_name_plural = "Social Media"

    def __str__(self):
        return f"{self.name} ({self.active})"

    def clean(self):
        errors: Dict[str, str] = {}

        if self.name:
            self.name = self.name.strip()

        if (
            self.name
            and SocialMedia.objects.filter(name__iexact=self.name)
            .exclude(pk=self.pk)
            .exists()
        ):
            errors["name"] = f"Social media with name '{self.name}' already exists."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
