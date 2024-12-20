# Generated by Django 5.1.4 on 2024-12-12 09:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ride_matching', '0002_driver_rating_riderequest_estimated_fare'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('CREATED', 'Created'), ('ACCEPTED', 'Accepted'), ('IN_PROGRESS', 'In Progress'), ('COMPLETED', 'Completed'), ('CANCELLED', 'Cancelled')], default='CREATED', max_length=20)),
                ('estimated_pickup_time', models.DateTimeField()),
                ('estimated_dropoff_time', models.DateTimeField()),
                ('actual_pickup_time', models.DateTimeField(blank=True, null=True)),
                ('actual_dropoff_time', models.DateTimeField(blank=True, null=True)),
                ('fare_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ride_matching.driver')),
                ('ride_request', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ride_matching.riderequest')),
            ],
        ),
    ]
