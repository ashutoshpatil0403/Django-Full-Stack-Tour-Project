# Generated by Django 5.0.3 on 2024-07-20 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour_app', '0022_user_booking_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_booking',
            name='travel_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]