# Generated by Django 4.2.9 on 2024-02-06 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_logged_in',
            field=models.BooleanField(default=False, null=True, verbose_name='is_logged_in'),
        ),
    ]
