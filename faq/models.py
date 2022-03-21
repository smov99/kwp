import uuid

from django.db import models
from proposal.models import BaseModel


class Section(BaseModel):
    order = models.IntegerField(blank=True, null=True)
    guid = models.CharField(max_length=64, blank=True, null=True)
    label = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return self.label

    def save(self, *args, **kwargs):
        if not self.guid:
            self.guid = uuid.uuid4().hex
        super(Section, self).save(*args, **kwargs)


class Article(BaseModel):
    order = models.IntegerField(blank=True, null=True)
    guid = models.CharField(max_length=64, blank=True, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('order',)
        verbose_name = 'Question'

    def __str__(self):
        return self.question

    def save(self, *args, **kwargs):
        if not self.guid:
            self.guid = uuid.uuid4().hex
        super(Article, self).save(*args, **kwargs)
