# Generated by Django 5.1.6 on 2025-02-19 05:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community_events', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='created_by',
        ),
        migrations.CreateModel(
            name='CommunityPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('post_type', models.CharField(choices=[('event', 'Event'), ('announcement', 'Announcement')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('event_date', models.DateField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Announcement',
        ),
        migrations.DeleteModel(
            name='Event',
        ),
    ]
