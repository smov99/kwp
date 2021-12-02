# Generated by Django 3.2 on 2021-12-02 07:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='section',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='section',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
