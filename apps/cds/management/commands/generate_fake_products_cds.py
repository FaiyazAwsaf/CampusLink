from django.core.management.base import BaseCommand
from apps.cds.models import CDS_Item  # Change this import if your app path is different
from faker import Faker
import random


class Command(BaseCommand):
    help = "Generate fake CDS items for testing"

    def handle(self, *args, **kwargs):
        fake = Faker()

        placeholder_image = "https://picsum.photos/seed/{}/400/300"
        categories = [
            "Electronics",
            "Books",
            "Food",
            "Clothing",
            "Stationery",
            "Sports Equipment",
        ]

        for _ in range(100):
            name = fake.unique.word().capitalize() + " " + random.choice(categories)
            description = fake.text(max_nb_chars=200)
            price = round(random.uniform(20, 500), 2)
            category = random.choice(categories)
            availability = random.choice([True, False])
            if random.random() < 0.8:
                image_url = placeholder_image.format(fake.uuid4())
            else:
                image_url = None

            CDS_Item.objects.create(
                name=name,
                description=description,
                price=price,
                image=image_url,
                availability=availability,
                category=category,
            )

        self.stdout.write(
            self.style.SUCCESS("Successfully created 100 fake CDS items!")
        )
