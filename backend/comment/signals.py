import os

from django.db.models.signals import pre_delete
from django.dispatch import receiver

from comment.models import Comment


@receiver(pre_delete, sender=Comment)
def delete_comment_image(sender, instance, **kwargs) -> None:
    if instance.attached_image and hasattr(instance.attached_image, "path"):
        if os.path.isfile(instance.attached_image.path):
            os.remove(instance.attached_image.path)
    if instance.attached_file and hasattr(instance.attached_file, "path"):
        if os.path.isfile(instance.attached_file.path):
            os.remove(instance.attached_file.path)
