from django.core.management.base import BaseCommand
from apps.entrepreneurs_hub.models import Owner
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Generate fake owners for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of owners to create (minimum 10, must be multiple of 10)'
        )

    def handle(self, *args, **kwargs):
        fake = Faker()
        count = kwargs['count']
        
        # Ensure minimum 10 and multiple of 10
        if count < 10:
            count = 10
        count = (count // 10) * 10
        
        self.stdout.write(f'Creating {count} fake owners...')

        placeholder_image = "https://picsum.photos/seed/{}/200/200"
        
        # Sample social media handles and websites
        social_domains = ['facebook.com', 'instagram.com']
        website_domains = ['shopify.com', 'wix.com', 'wordpress.com', 'github.io']

        for i in range(count):
            # Generate owner data
            first_name = fake.first_name()
            last_name = fake.last_name()
            full_name = f"{first_name} {last_name}"
            
            # 80% chance of having an image
            if random.random() < 0.8:
                image_url = placeholder_image.format(fake.uuid4())
            else:
                image_url = None
            
            # Generate bio (70% chance)
            if random.random() < 0.7:
                bio = fake.text(max_nb_chars=300)
            else:
                bio = None
            
            # Generate phone (90% chance)
            if random.random() < 0.9:
                phone = fake.phone_number()[:20]  # Limit to 20 chars
            else:
                phone = None
            
            # Generate email (95% chance)
            if random.random() < 0.95:
                email = fake.email()
            else:
                email = None
            
            # Generate social media URLs (60% chance each)
            facebook_url = None
            instagram_url = None
            website_url = None
            
            if random.random() < 0.6:
                username = first_name.lower() + last_name.lower()
                facebook_url = f"https://facebook.com/{username}"
            
            if random.random() < 0.6:
                username = first_name.lower() + last_name.lower()
                instagram_url = f"https://instagram.com/{username}"
            
            if random.random() < 0.4:
                domain = random.choice(website_domains)
                website_url = f"https://{first_name.lower()}{last_name.lower()}.{domain}"

            Owner.objects.create(
                name=full_name,
                image=image_url,
                bio=bio,
                phone=phone,
                email=email,
                facebook_url=facebook_url,
                instagram_url=instagram_url,
                website_url=website_url
            )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {count} fake owners!')
        )
