# Generated by Django 4.2.4 on 2023-09-17 09:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0007_alter_place_description_long'),
    ]

    operations = [
        migrations.RenameField(
            model_name='place',
            old_name='description_long',
            new_name='long_description',
        ),
        migrations.RenameField(
            model_name='place',
            old_name='description_short',
            new_name='short_description',
        ),
    ]
