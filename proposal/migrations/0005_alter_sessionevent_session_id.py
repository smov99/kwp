# Generated by Django 3.2 on 2021-05-19 22:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proposal', '0004_session_device'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessionevent',
            name='session_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='proposal.session'),
        ),
    ]
