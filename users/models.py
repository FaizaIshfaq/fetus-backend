from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name' 'phone_number', 'password']

    id = models.AutoField(
        "id",
        primary_key=True
    )
    first_name = models.CharField(
        "first_name",
        max_length=255,
    )
    last_name = models.CharField(
        "last_name",
        max_length=255,
        null=True,
        blank=True
    )
    email = models.CharField(
        "email",
        max_length=255,
        unique=True
    )
    phone_number = models.CharField(
        "phone_number",
        max_length=20,
        unique=True,
    )
    profile_image = models.ImageField(
        'profile_image',
        null=True,
        blank=True
    )
    password = models.CharField(
        'password',
        max_length=255,
    )
    is_logged_in = models.BooleanField(
        'is_logged_in',
        null=True,
        default=False
    )

    def __str__(self):
        return self.email
