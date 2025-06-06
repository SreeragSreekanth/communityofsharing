# Generated by Django 5.1.6 on 2025-02-21 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('borrow_requests', '0004_borrowrequest_lender_alter_borrowrequest_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowrequest',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('returned', 'Returned'), ('overdue', 'Overdue')], default='pending', max_length=10),
        ),
    ]
