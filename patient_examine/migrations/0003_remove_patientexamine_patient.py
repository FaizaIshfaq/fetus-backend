# Generated by Django 4.2.9 on 2024-04-14 15:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient_examine', '0002_alter_patientexamine_femur_pixel_depth_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patientexamine',
            name='patient',
        ),
    ]