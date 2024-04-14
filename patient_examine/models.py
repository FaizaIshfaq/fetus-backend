import os
from django.conf import settings
from django.db import models


class PatientFemurExamine(models.Model):
    id = models.AutoField(
        'id',
        primary_key=True
    )
    femur_image = models.ImageField(
        'femur_image'
    )
    pixel_depth = models.FloatField(
        'pixel_depth',
    )
    femur_length = models.IntegerField(
        'femur_length',
        null=True,
        blank=True
    )
    femur_age = models.IntegerField(
        'femur_age',
        null=True,
        blank=True
    )

    def delete(self, using=None, keep_parents=False):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.femur_image.name))
        super().delete(using, keep_parents)


class PatientHeadExamine(models.Model):
    id = models.AutoField(
        'id',
        primary_key=True
    )
    head_image = models.ImageField(
        'head_image'
    )
    pixel_depth = models.FloatField(
        'pixel_depth',
    )
    head_circumference = models.IntegerField(
        'femur_age',
        null=True,
        blank=True
    )
    gestational_age = models.IntegerField(
        'femur_age',
        null=True,
        blank=True
    )

    def delete(self, using=None, keep_parents=False):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.head_image.name))
        super().delete(using, keep_parents)
