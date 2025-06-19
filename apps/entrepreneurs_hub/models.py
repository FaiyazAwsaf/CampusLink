from django.db import models

class Storefront(models.Model):
    store_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default = "NiggaTown")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Storefront'
        verbose_name_plural = 'Storefronts'
        ordering = ['store_id']


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    store_id = models.ForeignKey(Storefront, on_delete = models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['name']