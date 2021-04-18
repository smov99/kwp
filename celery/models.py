from django.db import models


class Section(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    label = models.CharField(max_length=255)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.label


class Article(models.Model):
    order = models.IntegerField(blank=True, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return self.question
