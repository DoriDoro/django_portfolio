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
    url = models.URLField(max_length=250, null=True, blank=True)
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
    position = models.CharField(max_length=200)
    start_date = models.DateField(verbose_name=_("start date"))
    end_date = models.DateField(blank=True, null=True, verbose_name=_("end date"))
    until_present = models.BooleanField(default=False, verbose_name=_("present"))
    address = models.CharField(max_length=100, blank=True, null=True)
    job_type = models.CharField(
        max_length=14, choices=JobType, verbose_name=_("job type")
    )
    description = models.TextField()
    published = models.BooleanField(
        default=True, verbose_name=_("job visible on website")
    )
    skill = models.ManyToManyField("projects.Skill", related_name="job_skills")
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
        max_length=6,
        choices=LevelChoices,
        default=LevelChoices.A1,
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
    url = models.URLField(max_length=250, verbose_name=_("url of social media"))
    published = models.BooleanField(
        default=True, verbose_name=_("social media visible on website")
    )

    class Meta:
        verbose_name_plural = "SocialMedia"

    def __str__(self):
        return f"{self.name} ({self.published})"
