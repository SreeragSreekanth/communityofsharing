# Generated by Django 5.1.6 on 2025-02-15 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('borrow_requests', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='borrowrequest',
            old_name='created_at',
            new_name='requested_at',
        ),
        migrations.RemoveField(
            model_name='borrowrequest',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='borrowrequest',
            name='approved_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='borrowrequest',
            name='returned_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='borrowrequest',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('returned', 'Returned')], default='pending', max_length=10),
        ),
    ]
