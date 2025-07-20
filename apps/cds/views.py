from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import CDS_Item
from apps.accounts.decorators import cds_owner_required, login_required_json
import json

@require_http_methods(["GET"])
def get_cds_items(request):
    """
    Get all CDS items with enhanced information
    """
    try:
        items = CDS_Item.objects.all().values(
            'item_id',
            'name', 
            'description', 
            'price',
            'image',
            'availability',
        )
        items_list = list(items)
        
        # Convert Decimal to float for JSON serialization
        for item in items_list:
            item['price'] = float(item['price'])

        return JsonResponse({
            'success': True,
            'items': items_list,
            'total_count': len(items_list)
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'items': []
        }, status=500)

@require_http_methods(["GET"])
def get_cds_item_detail(request, item_id):
    """
    Get detailed information about a specific CDS item
    """
    try:
        item = CDS_Item.objects.get(item_id=item_id)
        item_data = {
            'item_id': item.item_id,
            'name': item.name,
            'description': item.description,
            'price': float(item.price),
            'image': item.image,
            'availability': item.availability,
            'stock_quantity': item.stock_quantity,
            'category': item.category,
            'created_at': item.created_at.isoformat() if item.created_at else None,
            'updated_at': item.updated_at.isoformat() if item.updated_at else None,
        }
        
        return JsonResponse({
            'success': True,
            'item': item_data
        })
    
    except CDS_Item.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Item not found'
        }, status=404)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
        
@csrf_exempt
@login_required_json
@require_http_methods(["POST"])
def add_to_cart(request):
    """
    Add item to cart (placeholder for future cart functionality)
    """
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = data.get('quantity', 1)
        
        # Validate item exists and is available
        try:
            item = CDS_Item.objects.get(item_id=item_id)
        except CDS_Item.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Item not found'
            }, status=404)
        
        # Check availability and stock
        if not item.availability or item.stock_quantity < quantity:
            return JsonResponse({
                'success': False,
                'error': 'Item not available or insufficient stock'
            }, status=400)
        
        # Tmplement actual cart functionality
        # For now, just return success
        return JsonResponse({
            'success': True,
            'message': f'Added {quantity} x {item.name} to cart',
            'item': {
                'item_id': item.item_id,
                'name': item.name,
                'price': float(item.price),
                'quantity': quantity
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)