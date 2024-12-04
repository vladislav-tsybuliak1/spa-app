from tkinter.constants import CASCADE

from django.conf import settings
from django.db import models

from comment.validators import validate_comment_text


class Comment(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    home_page = models.URLField(
        blank=True,
        null=True
    )
    text = models.TextField(validators=[validate_comment_text])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reply = models.ForeignKey(
        to="self",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="replies",
    )

    class Meta:
        ordering = ("-created_at",)
