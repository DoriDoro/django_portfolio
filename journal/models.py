from django.db import models
from django.db.models import Q
from django.db.models.functions import Lower
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField

from utils.database.managers import ActiveManager
from utils.database.slug import SlugCreateMixin
from utils.database.validators import validate_not_blank

# -- CONSTANT --
# -- Link Choices --
PANEL_CHOICES = ["JOURNAL", "PROJECT"]


# -- Custom Manager --
class JournalActivePublishedManager(models.Manager):
    """Filters to active=True and status=PUBLISHED entries."""

    def get_queryset(self):
        return super().get_queryset().filter(active=True, status=Journal.StatusChoices.PUBLISHED)


# -- Model definition --
class Journal(SlugCreateMixin, models.Model):
    """The steps of my projects."""

    class StatusChoices(models.TextChoices):
        DRAFT = "DF", _("Draft")
        PUBLISHED = "PB", _("Published")

    class CategoryChoices(models.TextChoices):
        BLOG = "BLOG", "blog"
        EPIC_EVENTS = "EPIC_EVENTS", "epic-events"
        JOURNAL = "JOURNAL", "journal"
        OC_LETTINGS = "OC_LETTINGS", "oc-lettings"
        PORTFOLIO = "PORTFOLIO", "portfolio"
        SOFT_DESK = "SOFT_DESK", "soft-desk"

    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, blank=True, unique=True, editable=True)
    status = models.CharField(
        max_length=2, choices=StatusChoices.choices, default=StatusChoices.DRAFT
    )
    content = HTMLField(validators=[validate_not_blank])
    category = models.CharField(max_length=11, choices=CategoryChoices.choices)

    published = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    links = models.ManyToManyField("journal.Link", blank=True, related_name="link_journals")

    objects = models.Manager()
    active_journals = ActiveManager()
    active_published_journals = JournalActivePublishedManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                name="uq_journal_name",
                violation_error_code="unique",
                violation_error_message="A Journal with that name exists already.",
            ),
            models.CheckConstraint(
                condition=~Q(status="PB") | Q(published__isnull=False),
                name="ck_journal_published_has_date",
                violation_error_code="check",
                violation_error_message="A published journal must have a publish date.",
            ),
        ]
        indexes = [
            models.Index(Lower("name"), "active", name="idx_journal_name_active"),
            models.Index(
                fields=["active", "status", "-published"],
                name="idx_journal_active_status_pub",
            ),
        ]
        ordering = ["-published", "-created"]

    def __str__(self):
        return self.name

    def _normalize_fields(self):
        if self.name:
            self.name = self.name.strip()

    def save(self, *args, **kwargs):
        """Pass clean=False to skip full_clean(); also regenerates slug when name changes."""
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
            self.create_unique_slug(Journal)
            if fields_to_update is not None:
                fields_to_update.add("slug")

        if fields_to_update is not None:
            kwargs["update_fields"] = list(fields_to_update)
        super().save(*args, **kwargs)

    def mark_published(self, commit: bool = True):
        """Set status to PUBLISHED and stamp the published timestamp; skips DB write if commit=False."""
        self.status = Journal.StatusChoices.PUBLISHED
        self.published = timezone.now()
        if commit:
            self.save(update_fields=["status", "published", "updated"])

    def get_absolute_url(self):
        return reverse("journal:journal-detail", kwargs={"slug": self.slug})


class Link(models.Model):
    """An external URL attached to a journal entry or project, scoped to a panel."""

    class PanelChoices(models.TextChoices):
        JOURNAL = "JOURNAL", "Journal"
        PROJECT = "PROJECT", "Project"

    title = models.CharField(max_length=200)
    url = models.URLField()
    panel = models.CharField(
        max_length=7, choices=PanelChoices.choices, default=PanelChoices.JOURNAL
    )

    active = models.BooleanField(default=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    platform = models.ForeignKey(
        "journal.Platform", on_delete=models.PROTECT, related_name="links"
    )

    objects = models.Manager()
    active_links = ActiveManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["platform", "url"],
                name="link_platform_url_unique",
                violation_error_code="unique",
                violation_error_message="This Link exists already.",
            ),
            models.UniqueConstraint(
                Lower("title"),
                "platform",
                name="uix_link_title_platform",
                violation_error_code="unique",
                violation_error_message="The title has to be unique per platform.",
            ),
            models.CheckConstraint(
                condition=Q(panel__in=PANEL_CHOICES),
                name="ck_link_panel",
                violation_error_code="check",
                violation_error_message="Panel choice does not exist.",
            ),
        ]
        indexes = [models.Index(fields=["active", "platform"], name="idx_link_active_platform")]
        ordering = [Lower("title"), "pk"]

    def __str__(self):
        return self.title

    def _normalize_fields(self):
        if self.title:
            self.title = self.title.strip()
        if self.url:
            self.url = self.url.strip()

    def save(self, *args, **kwargs):
        """Pass clean=False to skip full_clean(), e.g. in management commands."""
        clean = kwargs.pop("clean", True)
        self._normalize_fields()
        if clean:
            self.full_clean()
        super().save(*args, **kwargs)


class Platform(models.Model):
    """The origin platform of a link (e.g. GitHub, YouTube, LinkedIn)."""

    name = models.CharField(max_length=250)

    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                name="uq_platform_low_name",
                violation_error_code="unique",
                violation_error_message="This Platform exists already.",
            ),
        ]
        ordering = [Lower("name"), "pk"]

    def __str__(self):
        return self.name

    def _normalize_fields(self):
        if self.name:
            self.name = self.name.strip()

    def save(self, *args, **kwargs):
        """Pass clean=False to skip full_clean(), e.g. in management commands."""
        clean = kwargs.pop("clean", True)
        self._normalize_fields()
        if clean:
            self.full_clean()
        super().save(*args, **kwargs)
