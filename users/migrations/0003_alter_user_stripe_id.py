# Generated by Django 5.1 on 2025-01-14 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_stripe_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='stripe_id',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
