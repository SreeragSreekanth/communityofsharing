# Generated by Django 5.1.6 on 2025-02-21 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('borrow_requests', '0005_alter_borrowrequest_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowrequest',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('returned', 'Returned'), ('overdue', 'Overdue'), ('timed_out', 'Timed Out')], default='pending', max_length=10),
        ),
    ]
