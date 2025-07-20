from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import CDS_Item
from apps.accounts.decorators import cds_owner_required
import json


@csrf_exempt
@cds_owner_required
@require_http_methods(["POST"])
def create_cds_item(request):
    """
    Create a new CDS item (CDS Owner only)
    """
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['name', 'description', 'price']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({
                    'success': False,
                    'error': f'{field} is required'
                }, status=400)
        
        # Create item
        item = CDS_Item.objects.create(
            name=data['name'],
            description=data['description'],
            price=data['price'],
            image=data.get('image', ''),
            availability=data.get('availability', True)
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Item created successfully',
            'item': {
                'item_id': item.item_id,
                'name': item.name,
                'description': item.description,
                'price': float(item.price),
                'availability': item.availability
            }
        }, status=201)
        
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


@csrf_exempt
@cds_owner_required
@require_http_methods(["PUT"])
def update_cds_item(request, item_id):
    """
    Update a CDS item (CDS Owner only)
    """
    try:
        data = json.loads(request.body)
        
        try:
            item = CDS_Item.objects.get(item_id=item_id)
        except CDS_Item.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Item not found'
            }, status=404)
        
        # Update item fields
        if 'name' in data:
            item.name = data['name']
        if 'description' in data:
            item.description = data['description']
        if 'price' in data:
            item.price = data['price']
        if 'image' in data:
            item.image = data['image']
        if 'availability' in data:
            item.availability = data['availability']
        
        item.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Item updated successfully',
            'item': {
                'item_id': item.item_id,
                'name': item.name,
                'description': item.description,
                'price': float(item.price),
                'availability': item.availability
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


@cds_owner_required
@require_http_methods(["DELETE"])
def delete_cds_item(request, item_id):
    """
    Delete a CDS item (CDS Owner only)
    """
    try:
        try:
            item = CDS_Item.objects.get(item_id=item_id)
        except CDS_Item.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Item not found'
            }, status=404)
        
        item_name = item.name
        item.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Item "{item_name}" deleted successfully'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@cds_owner_required
@require_http_methods(["GET"])
def get_cds_analytics(request):
    """
    Get CDS analytics (CDS Owner only)
    """
    try:
        total_items = CDS_Item.objects.count()
        available_items = CDS_Item.objects.filter(availability=True).count()
        unavailable_items = total_items - available_items
        
        # Basic analytics
        analytics = {
            'total_items': total_items,
            'available_items': available_items,
            'unavailable_items': unavailable_items,
            'availability_rate': (available_items / total_items * 100) if total_items > 0 else 0
        }
        
        return JsonResponse({
            'success': True,
            'analytics': analytics
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
