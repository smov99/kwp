from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class CustomUser(AbstractUser):
    guid = models.CharField(primary_key=True, max_length=32, blank=True)
    email = models.EmailField('Email address', unique=True)
    email_confirmed = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def save(self, *args, **kwargs):

        if not self.guid:
            self.guid = uuid.uuid4().hex

        super(CustomUser, self).save(*args, **kwargs)
