# Generated by Django 2.2.5 on 2019-10-19 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circulation', '0007_auto_20191009_1830'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserve',
            name='description',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]