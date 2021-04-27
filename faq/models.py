from django.db import models


class Section(models.Model):
    order = models.IntegerField(blank=True, null=True)
    guid = models.CharField(max_length=64, blank=True, null=True)
    label = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return self.label


class Article(models.Model):
    order = models.IntegerField(blank=True, null=True)
    guid = models.CharField(max_length=64, blank=True, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return self.question
