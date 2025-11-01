from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from listings.models import Listing
import random


class Command(BaseCommand):
    help = "Seed the database with sample listings"

    def handle(self, *args, **kwargs):
        """Create a default host if not exists"""
        host, _ = User.objects.get_or_create(username="host1", defaults={"email": "host1@example.com"})

        sample_listings = [
            {"title": "Cozy Apartment in Nairobi", "description": "2 bedroom apartment near CBD", "price_per_night": 45.00, "location": "Nairobi"},
            {"title": "Beach House in Mombasa", "description": "Beautiful ocean view villa", "price_per_night": 120.00, "location": "Mombasa"},
            {"title": "Safari Lodge in Maasai Mara", "description": "Luxury lodge inside the park", "price_per_night": 200.00, "location": "Maasai Mara"},
        ]

        for data in sample_listings:
            listing, created = Listing.objects.get_or_create(
                title=data["title"],
                defaults={**data, "host": host}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created listing: {listing.title}"))
            else:
                self.stdout.write(self.style.WARNING(f"Listing already exists: {listing.title}"))
