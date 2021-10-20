import os

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
    with_error = models.CharField(max_length=64, default='No', choices=(
        ('Yes', 'Yes'),
        ('No', 'No')
    ))
    message = models.CharField(max_length=255, blank=True, null=True)
    client_ip = models.CharField(max_length=64, null=True)
    client_geolocation = models.CharField(max_length=255, blank=True, null=True)
    device = models.CharField(max_length=255, blank=True, null=True)

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
    error_type = models.CharField(max_length=20, default='Salesforce')
    api_call_type = models.CharField(max_length=255, blank=True, null=True)
    sf_object = models.CharField(max_length=255, blank=True, null=True)
    error = models.TextField(blank=True, null=True)


class SalesforceCategory(BaseModel):
    salesforce_category = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Salesforce categories"

    def __str__(self):
        return self.salesforce_category


class StaticResource(BaseModel):
    file_description = models.CharField(max_length=255, blank=True, null=True, unique=True)
    s3_file_location = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    document = models.FileField(null=True, blank=True)
    salesforce_category = models.ForeignKey(SalesforceCategory, on_delete=models.CASCADE)

    __original_document_name = None

    class Meta:
        unique_together = ('is_active', 'salesforce_category')

    def __init__(self, *args, **kwargs):
        super(StaticResource, self).__init__(*args, **kwargs)
        self.__original_document_name = self.document.name
        self.__original_file_description = self.file_description

    def __str__(self):
        return self.file_description

    def save(self, *args, **kwargs):
        if self.document:
            if self.document.name != self.__original_document_name:
                self.s3_file_location = f'{settings.KWP_S3_RESOURCES}{self.document.name}'
                try:
                    services.write_file_in_memory(self.document.path, self.document.file)
                except:
                    os.remove(self.document.path)
                    services.write_file_in_memory(self.document.path, self.document.file)
                services.s3_upload_file(self.document.name, 'static')
                os.remove(self.document.path)
            else:
                try:
                    services.s3_download_file(self.document.name, 'static')
                except FileExistsError:
                    pass
        else:
            self.is_active = False
            if self.s3_file_location:
                services.s3_delete_static_file(self.s3_file_location)
            self.s3_file_location = None
        super(StaticResource, self).save(*args, **kwargs)
