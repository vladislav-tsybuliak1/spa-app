import re

from django.core.exceptions import ValidationError


def validate_username(username: str) -> None:
    if re.search(r"^[0-9a-zA-Z]*$", username) is None:
        raise ValidationError(
            f"{username} contains invalid characters. Only letters and digits are allowed."
        )
    if len(username) <= 3:
        raise ValidationError("Too short username. It should be at least 3 characters.")
