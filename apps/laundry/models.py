from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class LaundryCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    wash_price = models.DecimalField(max_digits=7, decimal_places=2)
    iron_price = models.DecimalField(max_digits=7, decimal_places=2)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class LaundryInvoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items_json = models.JSONField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_date = models.DateField()
    order_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice {self.id} | User: {self.user.username} | Tk. {self.total_cost}"
