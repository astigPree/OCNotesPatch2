# Generated by Django 4.2.11 on 2024-06-14 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stickynote',
            name='gender',
            field=models.CharField(default='', max_length=2),
        ),
    ]