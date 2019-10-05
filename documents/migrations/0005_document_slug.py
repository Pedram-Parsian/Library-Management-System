# Generated by Django 2.2.5 on 2019-10-05 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0004_remove_document_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, unique=True),
        ),
    ]
