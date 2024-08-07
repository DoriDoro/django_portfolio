from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField


class DoriDoro(models.Model):
    user = models.ForeignKey(
        "accounts.User",
        null=True,
        on_delete=models.SET_NULL,
        related_name="doro_user",
        verbose_name=_("user instance"),
    )
    phone = models.CharField(max_length=14)
    address = models.CharField(max_length=150)
    profession = models.CharField(max_length=150)
    introduction = HTMLField()
    dream_job = HTMLField(verbose_name=_("dream job description"))
    free_time = HTMLField(verbose_name=_("after work description"))

    class Meta:
        verbose_name_plural = "DoriDoro"

    def __str__(self):
        return self.get_full_name

    @property
    def get_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Achievement(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    published = models.BooleanField(
        default=True, verbose_name=_("achievement visible on website")
    )

    def __str__(self):
        return f"{self.title} ({self.published})"


class Degree(models.Model):
    organization = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    published = models.BooleanField(
        default=True, verbose_name=_("degree visible on website")
    )

    def __str__(self):
        return f"{self.organization} ({self.published})"


class Fact(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    published = models.BooleanField(
        default=True, verbose_name=_("fact visible on website")
    )

    def __str__(self):
        return f"{self.title} ({self.published})"


class Hobby(models.Model):
    name = models.CharField(max_length=100)
    published = models.BooleanField(
        default=True, verbose_name=_("hobby visible on website")
    )

    class Meta:
        verbose_name_plural = "hobbies"

    def __str__(self):
        return f"{self.name} ({self.published})"


class Job(models.Model):
    # JOB_TYPE variables:
    FREELANCE = "FREELANCE"
    EMPLOYED = "EMPLOYED"
    APPRENTICESHIP = "APPRENTICESHIP"
    FORMATION = "FORMATION"
    MENTORING = "MENTORING"
    PARENTAL_LEAVE = "PARENTAL_LEAVE"
    SABBATICAL = "SABBATICAL"

    JOB_TYPES = [
        (FREELANCE, _("Freelance")),
        (EMPLOYED, _("Employed")),
        (APPRENTICESHIP, _("Apprenticeship")),
        (FORMATION, _("Formation")),
        (MENTORING, _("Mentoring")),
        (PARENTAL_LEAVE, _("Parental_Leave")),
        (SABBATICAL, _("Sabbatical")),
    ]

    company_name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    start_date = models.DateField(verbose_name=_("start date"))
    end_date = models.DateField(blank=True, null=True, verbose_name=_("end date"))
    until_present = models.BooleanField(default=False, verbose_name=_("until present"))
    address = models.CharField(max_length=100, blank=True, null=True)
    job_type = models.CharField(
        max_length=14, choices=JOB_TYPES, verbose_name=_("job type")
    )
    description = models.TextField()
    published = models.BooleanField(
        default=True, verbose_name=_("job visible on website")
    )
    tags = models.ManyToManyField("projects.Tag", related_name="job_tags")
    links = models.ManyToManyField("projects.Link", related_name="job_links")

    def __str__(self):
        return f"{self.job_type} ({self.company_name} - {self.published})"

    def clean(self):
        super().clean()

        if self.until_present and self.end_date is not None:
            raise ValidationError(
                _("If the job is ongoing, the end date should be empty.")
            )
        if not self.until_present and self.end_date is None:
            raise ValidationError(
                _("End date must be provided if the job is not ongoing.")
            )
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError(_("End date should be after start date."))


class Language(models.Model):
    # LEVEL_CHOICES variables:
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"
    C2 = "C2"
    NATIVE = "Native"

    LEVEL_CHOICES = [
        (A1, "A1"),
        (A2, "A2"),
        (B1, "B1"),
        (B2, "B2"),
        (C1, "C1"),
        (C2, "C2"),
        (NATIVE, _("Native Speaker")),
    ]

    name = models.CharField(max_length=50)
    level = models.CharField(
        max_length=7,
        choices=LEVEL_CHOICES,
        default=A1,
    )
    published = models.BooleanField(
        default=True, verbose_name=_("language visible on website")
    )

    def __str__(self):
        return f"{self.name} ({self.level} - {self.published})"


class Reference(models.Model):
    name = models.CharField(max_length=150)
    profession = models.CharField(max_length=250)
    email = models.EmailField(
        blank=True, null=True, max_length=250, verbose_name=_("email address")
    )
    phone = models.CharField(blank=True, null=True, max_length=14)
    language = models.CharField(max_length=100, verbose_name=_("spoken language"))
    published = models.BooleanField(
        default=True, verbose_name=_("reference visible on website")
    )

    def __str__(self):
        return f"{self.name} ({self.published})"


class SocialMedia(models.Model):
    name = models.CharField(max_length=150)
    url = models.URLField(max_length=250)
    published = models.BooleanField(
        default=True, verbose_name=_("social media visible on website")
    )

    class Meta:
        verbose_name_plural = "SocialMedia"

    def __str__(self):
        return f"{self.name} ({self.published})"
