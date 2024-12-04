# Generated by Django 5.1.4 on 2024-12-04 17:31

import user.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                max_length=31,
                unique=True,
                validators=[user.validators.validate_username],
            ),
        ),
    ]
