from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from .services import UserManager


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractBaseUser):
    guid = models.CharField(max_length=64, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    email_confirmed = models.BooleanField(default=False)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
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


class Session(BaseModel):
    proposalid = models.CharField(max_length=64)
    is_proposalexists = models.BooleanField(default=False)
    email = models.ForeignKey(User, to_field='email', on_delete=models.CASCADE)
    accountid = models.CharField(max_length=64, blank=True, null=True)
    is_emailvalid = models.BooleanField(default=False)
    contactid = models.CharField(max_length=64, blank=True, null=True)
    is_contactcreated = models.BooleanField(default=False)
    message = models.CharField(max_length=255)


class SessionEvent(BaseModel):
    OPEN_PDF = 'open_pdf'
    DOWNLOAD = 'download'
    CLOSING_PREVIEW = 'closing_preview'
    OPENING_OF_SECTION = 'opening_of_section'
    OPENING_OF_SECTIONS_LINE = 'opening_of_sections_line'
    CLICK_ON_SUBMIT_BUTTON = 'click_on_submit_button'

    EVENT_CHOICES = (
        (OPEN_PDF, 'Open PDF document for reviewing'),
        (DOWNLOAD, 'Download document'),
        (CLOSING_PREVIEW, 'Closing modal preview window'),
        (OPENING_OF_SECTION, 'Opening of section / accordion'),
        (OPENING_OF_SECTIONS_LINE, 'Opening of lines / accordions in section'),
        (CLICK_ON_SUBMIT_BUTTON, 'Click on submit button in section')
    )

    sessionid = models.ForeignKey(Session, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=255, choices=EVENT_CHOICES, default=OPEN_PDF)
    event_name = models.CharField(max_length=255)
    questionid = models.CharField(max_length=64, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
