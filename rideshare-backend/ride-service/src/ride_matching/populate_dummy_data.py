from django.core.management.base import BaseCommand
from ride_matching.models import Driver, Location
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Populates the database with dummy drivers and locations'

    def handle(self, *args, **kwargs):
        for i in range(10):
            location = Location.objects.create(
                latitude=Decimal(str(random.uniform(40.7, 40.8))),
                longitude=Decimal(str(random.uniform(-74.0, -73.9)))
            )
            
            Driver.objects.create(
                driver_id=f"DRIVER_{i+1}",
                current_location=location,
                is_available=random.choice([True, False])
            )
            
        self.stdout.write(self.style.SUCCESS('Successfully created dummy data'))
