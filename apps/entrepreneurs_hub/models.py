from django.db import models
from django.core.exceptions import ValidationError
from apps.accounts.models import User, Roles

class Storefront(models.Model):
    store_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default = "NiggaTown")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='storefronts')

    def __str__(self):
        return self.name
    
    def clean(self):
        """Validate that the storefront owner is an entrepreneur"""
        super().clean()
        if self.owner and self.owner.role != Roles.ENTREPRENEUR:
            raise ValidationError({
                'owner': 'Storefront owner must have entrepreneur role'
            })
    
    def save(self, *args, **kwargs):
        """Override save to ensure validation"""
        self.full_clean()
        super().save(*args, **kwargs)
    
    def can_add_products(self, user):
        """Check if a user can add products to this storefront"""
        return self.owner == user and user.role == Roles.ENTREPRENEUR
    
    class Meta:
        verbose_name = 'Storefront'
        verbose_name_plural = 'Storefronts'
        ordering = ['store_id']


class Product(models.Model):

    product_id = models.AutoField(primary_key=True)
    store_id = models.ForeignKey(Storefront, on_delete = models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.URLField(default='https://images.pexels.com/photos/789327/pexels-photo-789327.jpeg', blank=True, null=True)
    category = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    def is_owned_by(self, user):
        """Check if the product is owned by the given user"""
        return self.store_id.owner == user
    
    def clean(self):
        """Validate product data integrity"""
        super().clean()
        if self.store_id:
            # Ensure the storefront owner is an entrepreneur
            if self.store_id.owner.role != Roles.ENTREPRENEUR:
                raise ValidationError({
                    'store_id': 'Products can only be created in storefronts owned by entrepreneurs'
                })
    
    def save(self, *args, **kwargs):
        """Override save to ensure validation"""
        self.full_clean()
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['name']