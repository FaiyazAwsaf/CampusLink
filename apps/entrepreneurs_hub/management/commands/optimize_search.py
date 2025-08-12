from django.core.management.base import BaseCommand
from django.contrib.postgres.search import SearchVector
from apps.entrepreneurs_hub.models import Product

class Command(BaseCommand):
    help = 'Optimize search indexes and update search vectors'
    
    def handle(self, *args, **options):
        self.stdout.write('Updating search vectors...')
        
        for product in Product.objects.all():
            Product.objects.filter(pk=product.pk).update(
                search_vector=SearchVector('name', weight='A') + 
                             SearchVector('description', weight='B') + 
                             SearchVector('category', weight='C'),
                popularity_score=product.views * 0.1
            )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully optimized search indexes')
        )
