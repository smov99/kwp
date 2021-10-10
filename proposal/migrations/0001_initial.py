# Generated by Django 3.2 on 2021-10-10 10:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('proposal_id', models.CharField(max_length=64, null=True)),
                ('proposal_exists', models.BooleanField(default=False)),
                ('email', models.CharField(blank=True, max_length=64, null=True)),
                ('account_id', models.CharField(blank=True, max_length=64, null=True)),
                ('email_valid', models.BooleanField(default=False)),
                ('contact_id', models.CharField(blank=True, max_length=64, null=True)),
                ('contact_created', models.BooleanField(default=False)),
                ('message', models.CharField(blank=True, max_length=255, null=True)),
                ('client_ip', models.CharField(max_length=64, null=True)),
                ('client_geolocation', models.CharField(blank=True, max_length=255, null=True)),
                ('device', models.CharField(blank=True, max_length=64, null=True)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='StaticResource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('file_description', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('file_description_es', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('file_description_en', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('s3_file_location', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('document', models.FileField(blank=True, null=True, upload_to='')),
                ('salesforce_category', models.CharField(choices=[('Show_Case_Study__c', 'Show Case Study'), ('Show_Quick_Start_Guide__c', 'Show Quick Start Guide'), ('Show_Brochure__c', 'Show Brochure'), ('Show_Kiwapower_at_a_Glance_video__c', 'Show Kiwapower at a Glance video')], max_length=50, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SessionEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('document_name', models.CharField(blank=True, max_length=255, null=True)),
                ('event_type', models.CharField(max_length=255)),
                ('event_name', models.CharField(max_length=255)),
                ('message', models.TextField(blank=True, null=True)),
                ('session_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='proposal.session')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='ErrorLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('error_type', models.CharField(default='Salesforce', max_length=20)),
                ('api_call_type', models.CharField(blank=True, max_length=255, null=True)),
                ('sf_object', models.CharField(blank=True, max_length=255, null=True)),
                ('error', models.TextField(blank=True, null=True)),
                ('session_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='errors', to='proposal.session')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
