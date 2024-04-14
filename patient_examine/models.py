import os
from django.conf import settings
from django.db import models


class PatientExamine(models.Model):
    id = models.AutoField(
        'id',
        primary_key=True
    )
    femur_image = models.ImageField(
        'femur_image'
    )
    head_image = models.ImageField(
        'femur_image'
    )
    femur_pixel_depth = models.FloatField(
        'femur_pixel_depth',
    )
    head_pixel_depth = models.FloatField(
        'head_pixel_depth',
    )
    femur_number = models.IntegerField(
        'femur_number',
        null=True,
        blank=True,
        default=1
    )
    femur_length = models.IntegerField(
        'femur_length',
        null=True,
        blank=True
    )
    gestational_age = models.IntegerField(
        'gestational_age',
        null=True,
        blank=True
    )

    def delete(self, using=None, keep_parents=False):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.femur_image.name))
        os.remove(os.path.join(settings.MEDIA_ROOT, self.head_image.name))
        super().delete(using, keep_parents)
