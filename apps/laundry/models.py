from django.db import models
from django.utils import timezone
from apps.accounts.models import User
import uuid

class LaundryCategory(models.Model):
    """Model for laundry item categories"""
    name = models.CharField(max_length=100, unique=True)
    wash_price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Price in BDT (Tk.)')
    ironing_price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Price in BDT (Tk.)')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Laundry Category'
        verbose_name_plural = 'Laundry Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class LaundryOrderItem(models.Model):
    """Model for individual items in a laundry order"""
    category = models.ForeignKey(LaundryCategory, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    wash = models.BooleanField(default=False)
    ironing = models.BooleanField(default=False)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.ForeignKey('LaundryOrder', on_delete=models.CASCADE, related_name='items')
    
    def __str__(self):
        services = []
        if self.wash:
            services.append('Wash')
        if self.ironing:
            services.append('Ironing')
        return f"{self.quantity} x {self.category.name} ({', '.join(services)})"

class LaundryOrder(models.Model):
    """Model for laundry orders/invoices"""
    STATUS_CHOICES = (
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('delivered', 'Delivered'),
    )
    
    invoice_number = models.CharField(max_length=50, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_items = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')
    estimated_delivery_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Invoice #{self.invoice_number} - {self.user.name}"
    
    def save(self, *args, **kwargs):
        # Generate invoice number if it doesn't exist
        if not self.invoice_number:
            self.invoice_number = f"LDY-{uuid.uuid4().hex[:8].upper()}"
        
        # Calculate estimated delivery date if not set
        if not self.estimated_delivery_date:
            # Base: 3 days for first 10 items, +1 day for each additional 10 items
            base_days = 3
            additional_days = (self.total_items - 1) // 10
            delivery_days = base_days + additional_days
            self.estimated_delivery_date = timezone.now().date() + timezone.timedelta(days=delivery_days)
            
        super().save(*args, **kwargs)
