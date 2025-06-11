from django.shortcuts import render
from django.http import JsonResponse
from .models import CDS_Item

# Create your views here.
def get_cds_items(request):
    items = CDS_Item.objects.all().values()
    items_list = list(items)
    return JsonResponse({'items': items_list})
