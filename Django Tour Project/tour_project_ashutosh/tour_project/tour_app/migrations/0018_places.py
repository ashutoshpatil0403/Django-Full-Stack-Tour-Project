# Generated by Django 5.0.3 on 2024-07-19 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour_app', '0017_user_booking_user_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='Places',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place_name', models.CharField(blank=True, max_length=500)),
            ],
        ),
    ]
