# Generated by Django 3.2 on 2021-04-26 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]