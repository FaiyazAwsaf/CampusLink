from django.core.management.base import BaseCommand
from apps.entrepreneurs_hub.models import Product, Storefront
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Generate fake products for testing'

    def handle(self, *args, **kwargs):
        fake = Faker()

        placeholder_image = "https://picsum.photos/seed/{}/400/300"
        stores = list(Storefront.objects.filter(name__in=["IUTian's Waffle", "NiggaTown"]))

        for _ in range(100):

            if random.random() < 0.8:
                image_url = placeholder_image.format(fake.uuid4())
            else:
                image_url = None

            name = fake.catch_phrase()
            store_id = random.choice(stores)
            category = random.choice(["Clothing", "Gadgets", "Food"])
            description = fake.text(max_nb_chars=200)
            price = round(random.uniform(50, 999), 2)
            availability = random.choice([True, False])

            Product.objects.create(
                store_id=store_id,
                name=name,
                category=category,
                description=description,
                price=price,
                availability=availability,
                image = image_url
            )

        self.stdout.write(self.style.SUCCESS('Successfully created 100 fake products!'))
