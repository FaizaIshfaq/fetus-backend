from django.db import models
from doctors.models import Doctor
from patient_examine.models import PatientFemurExamine, PatientHeadExamine


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
    examine_by = models.ForeignKey(
        to=Doctor,
        on_delete=models.SET_NULL,
        null=True
    )
    femur_examine = models.ForeignKey(
        to=PatientFemurExamine,
        related_name='femur_examine',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    head_examine = models.ForeignKey(
        to=PatientHeadExamine,
        related_name='head_examine',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
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

    @property
    def name(self):
        return self.__str__()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
