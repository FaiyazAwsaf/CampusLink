from django.core.management.base import BaseCommand
from apps.entrepreneurs_hub.models import Product, Storefront
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Generate fake products for testing'

    def handle(self, *args, **kwargs):
        fake = Faker()

        store, _ = Storefront.objects.get_or_create(store_id=1)

        placeholder_image = "https://picsum.photos/seed/{}/400/300"

        for _ in range(100):

            if random.random() < 0.8:
                image_url = placeholder_image.format(fake.uuid4())
            else:
                image_url = None

            name = fake.catch_phrase()
            category = random.choice(["Clothing", "Gadgets", "Food"])
            description = fake.text(max_nb_chars=200)
            price = round(random.uniform(50, 999), 2)
            availability = random.choice([True, False])

            Product.objects.create(
                store_id=store,
                name=name,
                category=category,
                description=description,
                price=price,
                availability=availability,
                image = image_url
            )

        self.stdout.write(self.style.SUCCESS('Successfully created 100 fake products!'))
