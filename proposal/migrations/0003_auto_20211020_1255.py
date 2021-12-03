# Generated by Django 3.2 on 2021-10-20 16:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proposal', '0002_auto_20211014_1149'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesforceCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('salesforce_category', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Salesforce categories',
            },
        ),
        migrations.AlterField(
            model_name='staticresource',
            name='salesforce_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proposal.salesforcecategory'),
        ),
    ]