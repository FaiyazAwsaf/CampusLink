from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.postgres.search import SearchVector
from .models import Product

@receiver(post_save, sender=Product)
def update_search_vector(sender, instance, created, **kwargs):
    if kwargs.get('update_fields') and 'search_vector' in kwargs.get('update_fields', []):
        return
    
    if kwargs.get('update_fields') and 'popularity_score' in kwargs.get('update_fields', []):
        return
    
    Product.objects.filter(pk=instance.pk).update(
        search_vector=SearchVector('name', weight='A') + 
                     SearchVector('description', weight='B') + 
                     SearchVector('category', weight='C'),
        popularity_score=instance.views * 0.1
    )
