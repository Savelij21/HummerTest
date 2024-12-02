

from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField(max_length=15, unique=True, name="phone")
    invite_code = models.CharField(max_length=6, unique=True, name="invite_code")
    foreign_invite_code = models.CharField(max_length=6, null=True, blank=True, name="foreign_invite_code")









