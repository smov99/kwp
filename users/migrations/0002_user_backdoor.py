# Generated by Django 3.2 on 2021-11-13 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='backdoor',
            field=models.BooleanField(default=False),
        ),
    ]
