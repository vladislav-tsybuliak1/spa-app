import os
import uuid

from django.utils.text import slugify


def comment_image_file_path(comment, filename) -> str:
    _, extension = os.path.splitext(filename)
    filename = (
        f"{slugify(comment.created_at)}-{uuid.uuid4()}{extension}"
    )
    return os.path.join("uploads/comments/images/", filename)
