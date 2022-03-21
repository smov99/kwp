from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
import uuid


class UserManager(BaseUserManager):
    def create_user(self, email, guid=None, email_confirmed=False, full_name=None, password=None, is_active=True,
                    is_staff=False, is_admin=False, is_backdoor=False):
        if not email:
            raise ValueError("Users must have an email address")
        user_obj = self.model(
            email=self.normalize_email(email),
            full_name=full_name
        )
        if not guid:
            guid = uuid.uuid4().hex
        user_obj.set_password(password)
        user_obj.guid = guid
        user_obj.email_confirmed = email_confirmed
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.backdoor = is_backdoor
        user_obj.is_active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, full_name=None, password=None):
        user = self.create_user(
            email,
            full_name=full_name,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, email, full_name=None, password=None):
        user = self.create_user(
            email,
            full_name=full_name,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user

    def create_backdoor(self, email, full_name=None, password=None):
        user = self.create_user(
            email,
            full_name=full_name,
            password=password,
            is_staff=True,
            is_backdoor=True
        )
        return user


class User(AbstractBaseUser):
    guid = models.CharField(max_length=64, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    email_confirmed = models.BooleanField(default=False)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    backdoor = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.is_admin:
            return True
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_backdoor(self):
        return self.backdoor
