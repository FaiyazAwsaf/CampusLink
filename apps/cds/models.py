from django.db import models

from django.conf import settings

class CDS_Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(max_length=500, blank=True, null=True, help_text="URL to item image")
    availability = models.BooleanField(default=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "CDS Item"
        verbose_name_plural = "CDS Items"
        ordering = ['name']

class CDSOrder(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Cash on Pick Up'),
        ('bkash', 'bKash'),
    ]
    DELIVERY_STATUS_CHOICES = [
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    delivery_status = models.CharField(max_length=20, choices=DELIVERY_STATUS_CHOICES, default='preparing')

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class CDSOrderItem(models.Model):
    order = models.ForeignKey(CDSOrder, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(CDS_Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"