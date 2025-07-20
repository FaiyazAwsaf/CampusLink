from django.db import models

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