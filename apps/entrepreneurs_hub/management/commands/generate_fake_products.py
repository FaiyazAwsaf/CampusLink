from django.core.management.base import BaseCommand
from apps.entrepreneurs_hub.models import Product, Storefront
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Generate fake products for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=100,
            help='Number of products to create'
        )

    def handle(self, *args, **kwargs):
        fake = Faker()
        count = kwargs['count']

        # Get all storefronts to assign products to
        stores = list(Storefront.objects.all())
        if not stores:
            self.stdout.write(
                self.style.ERROR('No storefronts found! Please run generate_fake_storefronts first.')
            )
            return

        self.stdout.write(f'Creating {count} fake products...')

        placeholder_image = "https://picsum.photos/seed/{}/400/300"
        
        # Expanded categories
        categories = [
            "Electronics", "Clothing", "Food & Beverages", "Books & Stationery",
            "Sports & Fitness", "Beauty & Health", "Home & Garden", "Toys & Games",
            "Automotive", "Jewelry & Accessories", "Art & Crafts", "Music & Instruments"
        ]

        # Product name templates by category
        product_templates = {
            "Electronics": ["Smart {}", "Digital {}", "Wireless {}", "Portable {}", "Gaming {}"],
            "Clothing": ["Casual {}", "Formal {}", "Vintage {}", "Designer {}", "Comfortable {}"],
            "Food & Beverages": ["Fresh {}", "Organic {}", "Homemade {}", "Premium {}", "Healthy {}"],
            "Books & Stationery": ["Academic {}", "Professional {}", "Creative {}", "Essential {}", "Quality {}"],
            "Sports & Fitness": ["Professional {}", "Training {}", "Outdoor {}", "Fitness {}", "Athletic {}"],
            "Beauty & Health": ["Natural {}", "Premium {}", "Organic {}", "Professional {}", "Essential {}"],
        }

        for _ in range(count):
            # 80% chance of having an image
            if random.random() < 0.8:
                image_url = placeholder_image.format(fake.uuid4())
            else:
                image_url = None

            # Select category and generate appropriate name
            category = random.choice(categories)
            if category in product_templates:
                template = random.choice(product_templates[category])
                name = template.format(fake.word().title())
            else:
                name = fake.catch_phrase()

            store_id = random.choice(stores)
            description = fake.text(max_nb_chars=200)
            price = round(random.uniform(50, 999), 2)
            availability = random.choice([True, True, True, False])  # 75% available
            views = random.randint(0, 500)
            popularity_score = random.uniform(0.0, 10.0)

            Product.objects.create(
                store_id=store_id,
                name=name,
                category=category,
                description=description,
                price=price,
                availability=availability,
                image=image_url,
                views=views,
                popularity_score=popularity_score
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} fake products!'))
