from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models

from comment.utils import comment_image_file_path
from comment.validators import validate_comment_text


class Comment(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    home_page = models.URLField(blank=True, null=True)
    text = models.TextField(validators=[validate_comment_text])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    attached_image = models.ImageField(
        blank=True,
        null=True,
        upload_to=comment_image_file_path,
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "jpg",
                    "gif",
                    "png",
                ]
            )
        ],
    )
    parent = models.ForeignKey(
        to="self",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="replies",
    )

    class Meta:
        ordering = ("-created_at",)
