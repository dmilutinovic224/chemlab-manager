from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True)
    institution = models.CharField(max_length=200, blank=True)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.email or self.username
# Create your models here.
