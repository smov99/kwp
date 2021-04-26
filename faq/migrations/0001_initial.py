# Generated by Django 3.2 on 2021-04-26 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('label', models.CharField(max_length=255)),
                ('label_es', models.CharField(max_length=255, null=True)),
                ('label_en', models.CharField(max_length=255, null=True)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(blank=True, null=True)),
                ('question', models.TextField()),
                ('question_es', models.TextField(null=True)),
                ('question_en', models.TextField(null=True)),
                ('answer', models.TextField()),
                ('answer_es', models.TextField(null=True)),
                ('answer_en', models.TextField(null=True)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faq.section')),
            ],
            options={
                'ordering': ('order',),
            },
        ),
    ]