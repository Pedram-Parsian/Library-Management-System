# Generated by Django 2.2.5 on 2019-10-30 18:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0010_document_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='email',
        ),
        migrations.RemoveField(
            model_name='review',
            name='name',
        ),
    ]
