from django.db import models


class Section(models.Model):
    guid = models.CharField(max_length=255, primary_key=True, unique=True)
    order = models.IntegerField()
    label = models.CharField(max_length=255)


class Article(models.Model):
    guid = models.CharField(max_length=255, primary_key=True, unique=True)
    order = models.IntegerField()
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
