# Generated by Django 5.1.6 on 2025-02-11 05:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0004_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='phone_number',
        ),
    ]
