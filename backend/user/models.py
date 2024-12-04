from django.contrib.auth.models import AbstractUser
from django.db import models

from user.validators import validate_username


class User(AbstractUser):
    username = models.CharField(
        max_length=31,
        unique=True,
        validators=[validate_username],
    )
    email = models.EmailField(unique=True)
