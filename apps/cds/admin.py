from django.contrib import admin
from .models import CDS_Item, CDSOrder, CDSOrderItem

# Register your models here.
admin.site.register(CDS_Item)
admin.site.register(CDSOrder)
admin.site.register(CDSOrderItem)
