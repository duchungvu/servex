from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    date_of_birth = models.DateField(blank=True)
    points = models.IntegerField(blank=True)

    def __str__(self):
        return self.user.username