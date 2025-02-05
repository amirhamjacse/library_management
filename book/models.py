from django.db import models
from django.conf import settings
from datetime import timedelta
from django.utils import timezone


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


class Borrow(models.Model):
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    borrowed_at = models.DateTimeField(
        auto_now_add=True
    )
    return_deadline = models.DateTimeField()
    returned_at = models.DateTimeField(
        null=True, blank=True
    )
    fine = models.DecimalField(
        max_digits=5, decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"Book: {self.book.title}, Borrowed by: {self.user.username}"

    def is_overdue(self):
        return self.return_deadline < timezone.now() and not self.returned_at

    def calculate_fine(self):
        if self.is_overdue():
            overdue_days = (timezone.now() - self.return_deadline).days
            self.fine = overdue_days * 5
            self.save()
        return self.fine
