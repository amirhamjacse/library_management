from django.db import models
from django.conf import settings


class Book(models.Model):
    title = models.CharField(
        null=False, blank=False,
        max_length=255
        )
    author = models.CharField(
        null=False, blank=False,
        max_length=255
        )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="books",
        null=True,
        blank=True
    )
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} by {self.author} - {'Available' if self.is_available else 'Not Available'}"
