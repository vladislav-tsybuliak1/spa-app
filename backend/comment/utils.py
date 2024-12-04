import os
import uuid

from django.utils.text import slugify


def comment_image_file_path(crew, filename) -> str:
    _, extension = os.path.splitext(filename)
    filename = (
        f"{slugify(crew.first_name)}"
        f"-{slugify(crew.last_name)}"
        f"-{uuid.uuid4()}{extension}"
    )
    return os.path.join("uploads/comments/images/", filename)
