from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import CDS_Item
from django.core.paginator import Paginator
from django.db.models import Q
from .models import CDS_Item
from apps.accounts.decorators import cds_owner_required, login_required_json
import json

@require_http_methods(["GET"])
def get_cds_items(request):
    try:
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 12))  

        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        category = request.GET.get('category')
        availability = request.GET.get('availability')
        sort_by = request.GET.get('sort_by') 
        search_query = request.GET.get('search', '').strip()


        items_qs = CDS_Item.objects.all()
        
        if search_query:
            items_qs = items_qs.filter(
                Q(name__icontains=search_query) | Q(category__icontains=search_query)
        )

        if sort_by == 'price_asc':
            items_qs = items_qs.order_by('price')
        elif sort_by == 'price_desc':
            items_qs = items_qs.order_by('-price')

        if min_price:
            items_qs = items_qs.filter(price__gte=float(min_price))
        if max_price:
            items_qs = items_qs.filter(price__lte=float(max_price))

        if category:    
            items_qs = items_qs.filter(category=category)

        if availability is not None:
            if availability.lower() in ["1", "true", "yes"]:
                items_qs = items_qs.filter(availability=True)
            elif availability.lower() in ["0", "false", "no"]:
                items_qs = items_qs.filter(availability=False)

        # --- Pagination ---
        paginator = Paginator(items_qs, page_size)
        page_obj = paginator.get_page(page)

        items_list = [
            {
                "item_id": item.item_id,
                "name": item.name,
                "category": item.category,
                "description": item.description,
                "price": float(item.price),
                "image": item.image,
                "availability": item.availability,
                "sort_by": sort_by,
            }
            for item in page_obj.object_list
        ]

        return JsonResponse({
            "success": True,
            "items": items_list,
            "total_count": paginator.count,
            "total_pages": paginator.num_pages,
            "current_page": page_obj.number,
            "page_size": page_size,
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e),
            "items": []
        }, status=500)
 
 
@require_http_methods(["GET"])
def get_cds_categories(request):
    cats = CDS_Item.objects.values_list('category', flat=True)
    unique_cats = set()
    for c in cats:
        if c:
            unique_cats.add(c.strip())
    return JsonResponse({'categories': sorted(unique_cats)})


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