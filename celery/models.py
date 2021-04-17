from django.db import models


class Section(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    label = models.CharField(max_length=255)


class Article(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    guid = models.CharField(max_length=255, unique=True)
    section = models.ForeignKey(Section, to_field=id, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
