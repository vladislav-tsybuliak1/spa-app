from PIL import Image
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models

from comment.utils import comment_image_file_path, comment_text_file_path
from comment.validators import validate_comment_text, validate_file_size


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
    attached_fild = models.FileField(
        blank=True,
        null=True,
        upload_to=comment_text_file_path,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["txt"]
            ),
            validate_file_size,
        ]
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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.attached_image:
            self.resize_image()

    def resize_image(self):
        img = Image.open(self.attached_image.path)
        img.thumbnail((320, 240))
        img.save(self.attached_image.path)
