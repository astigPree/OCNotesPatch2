# Generated by Django 4.2.11 on 2024-06-14 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_stickynote_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stickynote',
            name='gender',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]