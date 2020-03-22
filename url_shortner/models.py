import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse_lazy
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField

from url_shortner.tasks import extract_title_from_url


def url_identifier_generator():
    identifier = uuid.uuid4().hex[:4]

    while Url.objects.filter(url_identifier=identifier).exists():
        identifier = uuid.uuid4().hex[:4]

    return identifier


class Url(models.Model):
    """
    Description: URL Model
    """

    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()

    title = models.CharField(max_length=400, null=True, blank=True)
    original_url = models.URLField(verbose_name="URL", max_length=400)
    url_identifier = models.CharField(max_length=200, default=url_identifier_generator)
    access_count = models.IntegerField(default=0)

    class Meta:
        pass

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.title is None:
            extract_title_from_url.delay(self.pk)

        return self

    def get_absolute_url(self):
        return reverse_lazy(
            "urls:detail", kwargs={"url_identifier": self.url_identifier}
        )

    @property
    def shortened_url(self):
        return f"{settings.BASE_APP_URL}/{self.url_identifier}"  # noqa

    def increment_access_count(self):
        self.access_count += 1
        self.save()
