# Generated by Django 4.2.9 on 2024-04-11 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0003_alter_patient_gender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='gender',
        ),
    ]