from django.contrib.auth.models import BaseUserManager
import kwp.settings as settings

import uuid

SF_LOGIN_URL = 'https://test.salesforce.com/services/oauth2/token'
SF_CONSUMER_SECRET = 'CD74EE798586E68841BF6CFC60B61B451449904ACDFA3B9E6457D852954FF6B9'
SF_CONSUMER_KEY = '3MVG9M43irr9JAuyX9k4MSEg2sKpL9Eswc9hslkN7vnqYMZxFkIUreh4BiO3HhC..dq9GsWnIqebJDxzQ0CYO'
SF_INITIAL_ACCESS_TOKEN = 'ge0s0ft99'
SF_USER_NAME = 'smorozov@gmail.com'
SF_API_VERSION = 'v51.0'


class UserManager(BaseUserManager):
    def create_user(self, email, guid=None, email_confirmed=False, full_name=None, password=None, is_active=True,
                    is_staff=False, is_admin=False):
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
