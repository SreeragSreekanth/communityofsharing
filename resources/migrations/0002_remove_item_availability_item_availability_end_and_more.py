# Generated by Django 5.1.6 on 2025-02-11 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='availability',
        ),
        migrations.AddField(
            model_name='item',
            name='availability_end',
            field=models.DateField(blank=True, help_text='End date of availability', null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='availability_start',
            field=models.DateField(blank=True, help_text='Start date of availability', null=True),
        ),
    ]
