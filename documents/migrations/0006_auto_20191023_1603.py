# Generated by Django 2.2.5 on 2019-10-23 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0005_auto_20191023_1554'),
    ]

    operations = [
        migrations.RenameField(
            model_name='publisher',
            old_name='title',
            new_name='name',
        ),
    ]