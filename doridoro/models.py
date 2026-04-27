from django.db import models
from django.db.models import F, Q
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _

from utils.manager.managers import ActiveManager

# --- CONSTANTS: Language model ---
LANGUAGE_CHOICES = ["A1", "A2", "B1", "B2", "C1", "C2", "Native"]
ALL_JOB_TYPE_CHOICES = [
    "FREELANCE",
    "EMPLOYED",
    "APPRENTICESHIP",
    "FORMATION",
    "MENTORING",
    "PARENTAL_LEAVE",
    "SABBATICAL",
]
SELECTED_JOB_TYPE_CHOICES = ["EMPLOYED", "APPRENTICESHIP", "FORMATION"]


class Achievement(models.Model):
    """Challenges and Milestones."""

    title = models.CharField(max_length=300)
    content = models.CharField(max_length=500)

    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # --- Managers ---
    objects = models.Manager()
    active_achievements = ActiveManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("title"),
                name="uq_achieve_low_title",
                violation_error_code="unique",
                violation_error_message="An achievement already exists.",
            )
        ]
        ordering = [Lower("title"), "pk"]

    def __str__(self):
        return f"{self.title} ({self.active})"

    def _normalize_fields(self):
        if self.title:
            self.title = self.title.strip()

    def save(self, *args, **kwargs):
        clean = kwargs.pop("clean", True)
        self._normalize_fields()
        if clean:
            self.full_clean()
        super().save(*args, **kwargs)


class Degree(models.Model):
    """Reached degrees."""

    organization = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    url = models.URLField(max_length=250, blank=True, default="")

    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active_degrees = ActiveManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("organization"),
                Lower("degree"),
                name="uq_degree_low_orga_degree",
                violation_error_code="unique",
                violation_error_message="This organization-degree combination exists already.",
            ),
        ]
        ordering = [Lower("organization"), "pk"]

    def __str__(self):
        return f"{self.organization} ({self.active})"

    def _normalize_fields(self):
        if self.organization:
            self.organization = self.organization.strip()
        if self.degree:
            self.degree = self.degree.strip()

    def save(self, *args, **kwargs):
        clean = kwargs.pop("clean", True)
        self._normalize_fields()
        if clean:
            self.full_clean()
        super().save(*args, **kwargs)


class Fact(models.Model):
    """Short details to inform."""

    title = models.CharField(max_length=100)
    content = models.CharField(max_length=500)

    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active_facts = ActiveManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("title"),
                name="uq_fact_low_title",
                violation_error_code="unique",
                violation_error_message="A Fact with this title exists already.",
            )
        ]
        ordering = [Lower("title"), "pk"]

    def __str__(self):
        return f"{self.title} ({self.active})"

    def _normalize_fields(self):
        if self.title:
            self.title = self.title.strip()
        if self.content:
            self.content = self.content.strip()

    def save(self, *args, **kwargs):
        clean = kwargs.pop("clean", True)
        self._normalize_fields()
        if clean:
            self.full_clean()
        super().save(*args, **kwargs)


class Job(models.Model):

    class JobTypeChoices(models.TextChoices):
        FREELANCE = "FREELANCE", _("Freelance")
        EMPLOYED = "EMPLOYED", _("Employed")
        APPRENTICESHIP = "APPRENTICESHIP", _("Apprenticeship")
        FORMATION = "FORMATION", _("Formation")
        MENTORING = "MENTORING", _("Mentoring")
        PARENTAL_LEAVE = "PARENTAL_LEAVE", _("Parental Leave")
        SABBATICAL = "SABBATICAL", _("Sabbatical")

    company_name = models.CharField(max_length=200, blank=True, default="")
    address = models.CharField(max_length=100, blank=True, default="")
    position = models.CharField(max_length=200)
    description = models.JSONField(default=list)
    job_type = models.CharField(max_length=14, choices=JobTypeChoices.choices)

    start_date = models.DateField(verbose_name=_("start date"))
    end_date = models.DateField(blank=True, null=True, verbose_name=_("end date"))
    until_present = models.BooleanField(default=False, verbose_name=_("present"))

    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    skill = models.ManyToManyField("projects.Skill", related_name="jobs")
    links = models.ManyToManyField("projects.Link", related_name="jobs")

    objects = models.Manager()
    active_jobs = ActiveManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("position"),
                Lower("company_name"),
                "start_date",
                name="uq_job_position_company_start",
                violation_error_code="unique",
                violation_error_message="This position-company-start combination exists already.",
            ),
            models.CheckConstraint(
                check=Q(until_present=True) | Q(end_date__isnull=False),
                name="ck_job_present_end",
                violation_error_code="check",
                violation_error_message="End date must be provided if the job is not ongoing.",
            ),
            models.CheckConstraint(
                check=~Q(until_present=True) | Q(end_date__isnull=True),
                name="ck_job_present_no_end",
                violation_error_code="check",
                violation_error_message="If the job is ongoing, the end date should be empty.",
            ),
            models.CheckConstraint(
                check=Q(job_type__in=ALL_JOB_TYPE_CHOICES),
                name="ck_job_type",
                violation_error_code="check",
                violation_error_message="This job type does not exist.",
            ),
            models.CheckConstraint(
                check=~Q(job_type__in=SELECTED_JOB_TYPE_CHOICES)
                | Q(company_name__isnull=False),
                name="ck_job_selected_type_company",
                violation_error_code="check",
                violation_error_message="With this job_type a company_name has to be filled out.",
            ),
            models.CheckConstraint(
                check=Q(end_date__gte=F("start_date")) | Q(end_date__isnull=True),
                name="ck_job_start_before_end",
                violation_error_code="check",
                violation_error_message="End date should be after start date.",
            ),
        ]
        ordering = [Lower("position"), "pk"]

    def __str__(self):
        return f"{self.job_type} ({self.company_name} - {self.active})"

    def _normalize_fields(self):
        if self.position:
            self.position = self.position.strip()
        if self.company_name:
            self.company_name = self.company_name.strip()
        if self.address:
            self.address = self.address.strip()

    def save(self, *args, **kwargs):
        clean = kwargs.pop("clean", True)
        self._normalize_fields()
        if clean:
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

    name = models.CharField(max_length=50)
    level = models.CharField(
        max_length=6, choices=LevelChoices.choices, default=LevelChoices.A1
    )

    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active_languages = ActiveManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                name="uix_lang_low_name",
                violation_error_code="unique",
                violation_error_message="This language already exists.",
            ),
            models.CheckConstraint(
                name="ck_lang_level_valid",
                check=Q(level__in=[l for l in LANGUAGE_CHOICES]),
                violation_error_code="check",
                violation_error_message="This language level does not exist.",
            ),
        ]
        ordering = [Lower("name"), "pk"]

    def __str__(self):
        return f"{self.name} ({self.level} - {self.active})"

    def _normalize_fields(self):
        if self.name:
            self.name = self.name.strip()

    def save(self, *args, **kwargs):
        clean = kwargs.pop("clean", True)
        self._normalize_fields()
        if clean:
            self.full_clean()
        super().save(*args, **kwargs)


class SocialMedia(models.Model):
    """Links to my SocialMedia."""

    name = models.CharField(max_length=150)
    url = models.URLField(max_length=250)

    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active_social_medias = ActiveManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                name="uix_social_media_low_name",
                violation_error_code="unique",
                violation_error_message="This social media already exists.",
            ),
        ]
        ordering = [Lower("name"), "pk"]
        verbose_name_plural = "Social Media"

    def __str__(self):
        return f"{self.name} ({self.active})"

    def _normalize_fields(self):
        if self.name:
            self.name = self.name.strip()

    def save(self, *args, **kwargs):
        clean = kwargs.pop("clean", True)
        self._normalize_fields()
        if clean:
            self.full_clean()
        super().save(*args, **kwargs)
