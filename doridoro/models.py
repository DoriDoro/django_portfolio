from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class DoriDoro(models.Model):
    user = models.ForeignKey(
        "accounts.User",
        null=True,
        on_delete=models.SET_NULL,
        related_name="doro_user",
        verbose_name=_("user of DoriDoro"),
    )
    phone = models.CharField(max_length=14, verbose_name=_("phone of DoriDoro"))
    address = models.CharField(max_length=150, verbose_name=_("address of DoriDoro"))
    profession = models.CharField(
        max_length=150, verbose_name=_("profession of DoriDoro")
    )
    introduction = models.TextField(verbose_name=_("introduction of DoriDoro"))
    dream_job = models.TextField(verbose_name=_("dream job description of DoriDoro"))
    free_time = models.TextField(verbose_name=_("after work description of DoriDoro"))

    class Meta:
        verbose_name_plural = "DoriDoro"

    def __str__(self):
        return self.get_full_name

    @property
    def get_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Achievement(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("title of achievement"))
    content = models.TextField(verbose_name=_("content of achievement"))
    published = models.BooleanField(
        default=True, verbose_name=_("achievement visible on website")
    )

    def __str__(self):
        return f"{self.title} ({self.published})"


class Degree(models.Model):
    organization = models.CharField(
        max_length=100, verbose_name=_("organization of degree")
    )
    degree = models.CharField(max_length=100, verbose_name=_("degree"))
    published = models.BooleanField(
        default=True, verbose_name=_("degree visible on website")
    )

    def __str__(self):
        return f"{self.organization} ({self.published})"


class Fact(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("title of fact"))
    content = models.TextField(verbose_name=_("content of fact"))
    published = models.BooleanField(
        default=True, verbose_name=_("fact visible on website")
    )

    def __str__(self):
        return f"{self.title} ({self.published})"


class Hobby(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("name of hobby"))
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
        (MENTORING, _("MENTORING")),
        (PARENTAL_LEAVE, _("Parental_Leave")),
        (SABBATICAL, _("Sabbatical")),
    ]

    company_name = models.CharField(
        max_length=200, verbose_name=_("company name of the job")
    )
    position = models.CharField(max_length=200, verbose_name=_("position of the job"))
    start_date = models.DateField(verbose_name=_("start date of the job"))
    end_date = models.DateField(
        blank=True, null=True, verbose_name=_("end date of the job")
    )
    until_present = models.BooleanField(default=False, verbose_name=_("until present"))
    address = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="address of job"
    )
    job_type = models.CharField(
        max_length=14, choices=JOB_TYPES, verbose_name=_("type of job")
    )
    description = models.TextField(verbose_name=_("description of job"))
    published = models.BooleanField(
        default=True, verbose_name=_("job visible on website")
    )
    tags = models.ManyToManyField(
        "projects.Tag", related_name="job_tags", verbose_name=_("tags of the job")
    )
    links = models.ManyToManyField(
        "projects.Link", related_name="job_links", verbose_name="links of the job"
    )

    def __str__(self):
        return f"{self.job_type} ({self.company_name} - {self.published})"

    def clean(self):
        super().clean()

        if self.until_present and self.end_date is not None:
            raise ValidationError(
                _(
                    "If the job is ongoing (until present is True), the end date should be null"
                )
            )
        if not self.until_present and self.end_date is None:
            raise ValidationError(
                _(
                    "End date must be provided if the job is not ongoing (until_present is False)."
                )
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
        (A1, _("A1 (Beginner)")),
        (A2, _("A2 (Elementary)")),
        (B1, _("B1 (Intermediate)")),
        (B2, _("B2 (Upper Intermediate)")),
        (C1, _("C1 (Advanced)")),
        (C2, _("C2 (Proficient)")),
        (NATIVE, _("Native Speaker")),
    ]

    name = models.CharField(max_length=50, verbose_name=_("language"))
    level = models.CharField(
        max_length=7,
        choices=LEVEL_CHOICES,
        default=A1,
        verbose_name=_("level of language"),
    )
    published = models.BooleanField(
        default=True, verbose_name=_("language visible on website")
    )

    def __str__(self):
        return f"{self.name} ({self.level} - {self.published})"


class Reference(models.Model):
    name = models.CharField(max_length=150, verbose_name=_("name of reference"))
    profession = models.CharField(
        max_length=250, verbose_name=_("profession of reference")
    )
    email = models.EmailField(
        max_length=250, verbose_name=_("email address of reference")
    )
    phone = models.CharField(
        blank=True, max_length=14, verbose_name=_("phone of reference")
    )
    language = models.CharField(
        max_length=100, verbose_name=_("spoken language of reference")
    )
    published = models.BooleanField(
        default=True, verbose_name=_("reference visible on website")
    )

    def __str__(self):
        return f"{self.name} ({self.published})"


class SocialMedia(models.Model):
    name = models.CharField(max_length=150, verbose_name=_("name of social media"))
    url = models.URLField(max_length=250, verbose_name=_("url of social media"))
    published = models.BooleanField(
        default=True, verbose_name=_("social media visible on website")
    )

    class Meta:
        verbose_name_plural = "SocialMedia"

    def __str__(self):
        return f"{self.name} ({self.published})"


class Website(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("name of website"))
    url = models.URLField(max_length=250, verbose_name=_("url of website"))
    published = models.BooleanField(
        default=True, verbose_name=_("url visible on website")
    )

    def __str__(self):
        return f"{self.name} ({self.published})"
