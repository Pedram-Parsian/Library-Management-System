# Generated by Django 2.2.5 on 2019-10-23 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0004_auto_20191021_1922'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Publication',
            new_name='Publisher',
        ),
        migrations.RemoveField(
            model_name='document',
            name='publications',
        ),
        migrations.AddField(
            model_name='document',
            name='publisher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='documents.Publisher'),
        ),
    ]