# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class UserProfile(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    points = models.IntegerField(null=True, blank=True)


