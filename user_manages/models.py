from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUsers(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('member', 'Member'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')

    # Avoid conflicts by explicitly setting related_name
    groups = models.ManyToManyField(
        "auth.Group", related_name="customuser_groups", blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="customuser_permissions", blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
