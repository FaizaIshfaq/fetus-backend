from django.db import models


class Doctor(models.Model):

    class Gender(models.TextChoices):
        MALE = "m", "Male"
        FEMALE = "f", "Female"

    id = models.AutoField(
        'id',
        primary_key=True
    )
    name = models.CharField(
        'name',
        unique=True,
        max_length=255
    )
    gender = models.CharField(
        'gender',
        max_length=1,
        choices=Gender.choices
    )
    qualification = models.CharField(
        'qualification',
        max_length=255
    )
    specialization = models.CharField(
        'specialization',
        max_length=255
    )

    def __str__(self):
        return self.name
