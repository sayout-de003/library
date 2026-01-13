from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [('ADMIN', 'Admin'), ('MEMBER', 'Member')]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='MEMBER')
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
