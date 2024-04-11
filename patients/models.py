from django.db import models


class Patient(models.Model):

    class Trimester(models.TextChoices):
        FIRST = "1", "First"
        SECOND = "2", "Second"
        THIRD = "3", "Third"

    id = models.AutoField(
        'id',
        primary_key=True
    )
    first_name = models.CharField(
        'first_name',
        max_length=255,
    )
    last_name = models.CharField(
        'last_name',
        max_length=255,
    )
    date_of_birth = models.DateField(
        'date_of_birth',
        max_length=8
    )
    examine_date = models.DateField(
        'examine_date',
        max_length=8
    )
    trimester = models.CharField(
        'trimester',
        max_length=1,
        choices=Trimester.choices
    )
    blood_group = models.CharField(
        'blood_group',
        max_length=2
    )
    age = models.IntegerField(
        'age'
    )
    examine_by = models.CharField(
        "examine_by",
        max_length=255
    )
    email = models.CharField(
        "email",
        max_length=255,
        null=True,
        blank=True
    )
    phone_number = models.CharField(
        "phone_number",
        max_length=20
    )
    profile_image = models.ImageField(
        'profile_image',
        null=True,
        blank=True
    )
    is_active = models.BooleanField(
        'is_active',
        default=True
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
