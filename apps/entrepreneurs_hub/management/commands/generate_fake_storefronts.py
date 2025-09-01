from django.core.management.base import BaseCommand
from apps.entrepreneurs_hub.models import Owner, Storefront
from faker import Faker
import random
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Generate fake storefronts for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of storefronts to create (minimum 10, must be multiple of 10)'
        )

    def handle(self, *args, **kwargs):
        fake = Faker()
        count = kwargs['count']
        
        # Ensure minimum 10 and multiple of 10
        if count < 10:
            count = 10
        count = (count // 10) * 10
        
        self.stdout.write(f'Creating {count} fake storefronts...')

        # Get all owners to assign to storefronts
        owners = list(Owner.objects.all())
        if not owners:
            self.stdout.write(
                self.style.ERROR('No owners found! Please run generate_fake_owners first.')
            )
            return

        placeholder_image = "https://picsum.photos/seed/{}/400/300"
        
        # Sample store types and names
        store_types = [
            'Electronics', 'Fashion', 'Food & Beverage', 'Books & Stationery',
            'Sports & Fitness', 'Beauty & Health', 'Home & Garden', 'Toys & Games',
            'Automotive', 'Jewelry & Accessories'
        ]
        
        store_name_prefixes = [
            'Campus', 'Student', 'IUT', 'Tech', 'Smart', 'Quick', 'Fresh', 'Elite',
            'Prime', 'Urban', 'Modern', 'Classic', 'Digital', 'Creative', 'Innovative'
        ]
        
        store_name_suffixes = [
            'Store', 'Shop', 'Hub', 'Corner', 'Plaza', 'Market', 'Outlet', 'Express',
            'Zone', 'Center', 'Point', 'Station', 'Gallery', 'Emporium', 'Bazaar'
        ]

        # Campus locations
        locations = [
            'IUT Campus - Academic Building',
            'IUT Campus - Dormitory Area',
            'IUT Campus - Cafeteria Complex',
            'IUT Campus - Sports Complex',
            'IUT Campus - Library Building',
            'IUT Campus - Main Gate Area',
            'IUT Campus - Engineering Building',
            'IUT Campus - Student Center',
            'IUT Campus - Parking Area',
            'IUT Campus - Administrative Building'
        ]

        for i in range(count):
            # Generate store name
            prefix = random.choice(store_name_prefixes)
            suffix = random.choice(store_name_suffixes)
            store_name = f"{prefix} {suffix}"
            
            # Assign owner (some owners can have multiple stores)
            owner = random.choice(owners)
            
            # 85% chance of having an image
            if random.random() < 0.85:
                image_url = placeholder_image.format(fake.uuid4())
            else:
                image_url = 'https://images.pexels.com/photos/789327/pexels-photo-789327.jpeg'
            
            # Generate description (80% chance)
            if random.random() < 0.8:
                store_type = random.choice(store_types)
                description = f"A premier {store_type.lower()} store serving the IUT community. {fake.text(max_nb_chars=200)}"
            else:
                description = None
            
            # Generate established date (within last 5 years)
            if random.random() < 0.9:
                days_ago = random.randint(30, 1825)  # 30 days to 5 years
                established_date = date.today() - timedelta(days=days_ago)
            else:
                established_date = None
            
            # Assign location
            location = random.choice(locations)
            
            # Generate policies and info (70% chance each)
            return_policy = None
            shipping_info = None
            store_hours = None
            
            if random.random() < 0.7:
                return_policy = random.choice([
                    "7-day return policy for unused items with receipt.",
                    "14-day return policy. Items must be in original condition.",
                    "No returns on food items. 3-day return for other products.",
                    "Exchange only within 5 days of purchase.",
                    "Full refund within 10 days with original packaging."
                ])
            
            if random.random() < 0.7:
                shipping_info = random.choice([
                    "Free delivery within IUT campus. Same day delivery available.",
                    "Delivery available to dormitories. 2-3 hours delivery time.",
                    "Pick-up only from store location.",
                    "Free delivery for orders above ৳500. Otherwise ৳50 delivery charge.",
                    "Express delivery available for ৳100 extra."
                ])
            
            if random.random() < 0.8:
                store_hours = random.choice([
                    "Mon-Fri: 9:00 AM - 8:00 PM, Sat-Sun: 10:00 AM - 6:00 PM",
                    "Daily: 8:00 AM - 10:00 PM",
                    "Mon-Sat: 10:00 AM - 9:00 PM, Sun: Closed",
                    "Daily: 9:00 AM - 9:00 PM",
                    "Mon-Fri: 8:00 AM - 6:00 PM, Weekends: 10:00 AM - 4:00 PM"
                ])
            
            # Generate total sales (random between 0-1000)
            total_sales = random.randint(0, 1000)

            Storefront.objects.create(
                owner=owner,
                name=store_name,
                image=image_url,
                description=description,
                established_date=established_date,
                location=location,
                return_policy=return_policy,
                shipping_info=shipping_info,
                store_hours=store_hours,
                total_sales=total_sales
            )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {count} fake storefronts!')
        )
