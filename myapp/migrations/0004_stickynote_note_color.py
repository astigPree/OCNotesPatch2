# Generated by Django 4.2.11 on 2024-06-10 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_stickynote_emoji'),
    ]

    operations = [
        migrations.AddField(
            model_name='stickynote',
            name='note_color',
            field=models.PositiveSmallIntegerField(default=None),
        ),
    ]
