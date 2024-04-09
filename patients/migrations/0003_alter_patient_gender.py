# Generated by Django 4.2.9 on 2024-03-11 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0002_alter_patient_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='gender',
            field=models.CharField(choices=[('m', 'Male'), ('f', 'Female')], max_length=1, verbose_name='gender'),
        ),
    ]
