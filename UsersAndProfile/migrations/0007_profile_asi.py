# Generated by Django 4.1.6 on 2023-02-12 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UsersAndProfile', '0006_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='asi',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]