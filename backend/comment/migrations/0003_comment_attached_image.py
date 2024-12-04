# Generated by Django 5.1.4 on 2024-12-04 19:47

import comment.utils
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("comment", "0002_rename_reply_comment_parent"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="attached_image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=comment.utils.comment_image_file_path,
                validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["jpg", "gif", "png"]
                    )
                ],
            ),
        ),
    ]
