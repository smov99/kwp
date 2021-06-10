from django.db import models


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
    sf_error = models.CharField(max_length=255, blank=True, null=True)
