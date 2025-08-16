from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import CDSOrder, CDSOrderItem, CDS_Item
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q
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
        else:
            items_qs = items_qs.order_by('-item_id')

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
            "sort_by": sort_by,
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
            'category': item.category,
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
        
        # Check availability
        if not item.availability:
            return JsonResponse({
                'success': False,
                'error': 'Item not available'
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
    
# API endpoint to submit CDS order
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_cds_order(request):
    user = request.user
    items = request.data.get('items', [])
    payment_method = request.data.get('payment_method', 'cash')
    if not items:
        return Response({'error': 'No items provided.'}, status=status.HTTP_400_BAD_REQUEST)
    total_amount = 0
    order_items = []
    for item in items:
        try:
            product = CDS_Item.objects.get(pk=item.get('item_id'))
        except CDS_Item.DoesNotExist:
            continue
        quantity = item.get('quantity', 1)
        total_amount += float(product.price) * quantity
        order_items.append((product, quantity))
    delivery_status = request.data.get('delivery_status', 'preparing')
    order = CDSOrder.objects.create(user=user, payment_method=payment_method, total_amount=total_amount, delivery_status=delivery_status)
    for product, quantity in order_items:
        CDSOrderItem.objects.create(order=order, product=product, quantity=quantity)
    return Response({'success': True, 'order_id': order.id, 'total_amount': total_amount}, status=status.HTTP_201_CREATED)