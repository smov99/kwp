from django.db import models

import proposal.services as services
import kwp.settings as settings


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Session(BaseModel):
    proposal_id = models.CharField(max_length=64, null=True)
    proposal_exists = models.BooleanField(default=False)
    email = models.CharField(max_length=64, blank=True, null=True)
    account_id = models.CharField(max_length=64, blank=True, null=True)
    email_valid = models.BooleanField(default=False)
    contact_id = models.CharField(max_length=64, blank=True, null=True)
    contact_created = models.BooleanField(default=False)
    message = models.CharField(max_length=255, blank=True, null=True)
    client_ip = models.CharField(max_length=64, null=True)
    client_geolocation = models.CharField(max_length=255, blank=True, null=True)
    device = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return str(self.pk)


class SessionEvent(BaseModel):
    session_id = models.ForeignKey(
        Session,
        to_field='id',
        on_delete=models.CASCADE,
        related_name='events'
    )
    document_name = models.CharField(max_length=255, blank=True, null=True)
    event_type = models.CharField(max_length=255)
    event_name = models.CharField(max_length=255)
    message = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.event_name


class ErrorLog(BaseModel):
    session_id = models.ForeignKey(
        Session,
        to_field='id',
        on_delete=models.CASCADE,
        related_name='errors',
        blank=True,
        null=True
    )
    api_call_type = models.CharField(max_length=255, blank=True, null=True)
    sf_object = models.CharField(max_length=255, blank=True, null=True)
    sf_error = models.TextField(blank=True, null=True)


class StaticResources(BaseModel):
    file_description = models.CharField(max_length=255, blank=True, null=True, unique=True)
    s3_file_location = models.TextField(unique=True, blank=True, null=True)
    salesforce_file_id = models.CharField(max_length=255, unique=True)
    salesforce_category = models.CharField(
        max_length=50,
        unique=True,
        choices=tuple(
            (
                category,
                ' '.join(
                    category.split('__')[0].split('_'))
            ) for category in settings.STATIC_RESOURCES
        )
    )
    file_extension = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.file_description

    def save(self, *args, **kwargs):
        try:
            self.file_extension = services.get_static_resources_file(self.salesforce_file_id)
        finally:
            super(StaticResources, self).save(*args, **kwargs)
