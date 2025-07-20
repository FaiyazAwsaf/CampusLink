from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import LaundryCategory, LaundryOrder, LaundryOrderItem
from django.utils import timezone
from apps.accounts.decorators import laundry_staff_required
from apps.accounts.models import Roles
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from functools import wraps

@api_view(['GET'])
def get_laundry_categories(request):
    """Get all laundry categories with their prices"""
    categories = LaundryCategory.objects.all()
    data = [{
        'id': category.id,
        'name': category.name,
        'wash_price': float(category.wash_price),
        'ironing_price': float(category.ironing_price)
    } for category in categories]
    
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_laundry_order(request):
    """Create a new laundry order"""
    try:
        data = request.data
        items = data.get('items', [])
        
        if not items:
            return Response({'error': 'No items in order'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Calculate totals
        total_items = sum(item.get('quantity', 0) for item in items)
        total_amount = sum(float(item.get('subtotal', 0)) for item in items)
        
        # Create order
        order = LaundryOrder.objects.create(
            user=request.user,
            total_amount=total_amount,
            total_items=total_items,
            status='pending'
        )
        
        # Create order items        
        for item in items: 
            LaundryOrderItem.objects.create(
                order=order,
                category_id=item.get('category'),
                quantity=item.get('quantity', 1),
                wash=item.get('wash', False),
                ironing=item.get('ironing', False),
                subtotal=item.get('subtotal', 0)
            )
        
        # Return order details
        return Response({
            'invoice_number': order.invoice_number,
            'total_amount': float(order.total_amount),
            'total_items': order.total_items,
            'status': order.status,
            'estimated_delivery_date': order.estimated_delivery_date,
            'created_at': order.created_at
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_orders(request):
    """Get all laundry orders for the current user"""
    orders = LaundryOrder.objects.filter(user=request.user).order_by('-created_at')
    data = [{
        'id': order.id,
        'invoice_number': order.invoice_number,
        'total_amount': float(order.total_amount),
        'total_items': order.total_items,
        'status': order.status,
        'estimated_delivery_date': order.estimated_delivery_date,
        'created_at': order.created_at
    } for order in orders]
    
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_details(request, invoice_number):
    """Get details of a specific order"""
    try:
        order = LaundryOrder.objects.get(invoice_number=invoice_number, user=request.user)
        items = order.items.all()
        
        items_data = [{
            'category': item.category_id,
            'category_name': item.category.name,
            'quantity': item.quantity,
            'wash': item.wash,
            'ironing': item.ironing,
            'subtotal': float(item.subtotal)
        } for item in items]
        
        data = {
            'invoice_number': order.invoice_number,
            'total_amount': float(order.total_amount),
            'total_items': order.total_items,
            'status': order.status,
            'estimated_delivery_date': order.estimated_delivery_date,
            'created_at': order.created_at,
            'items': items_data
        }
        
        return Response(data)
    
    except LaundryOrder.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)


# Laundry Staff-only endpoints

def laundry_staff_api_required(view_func):
    """Decorator to convert laundry_staff_required for DRF views"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({
                'success': False,
                'error': 'Authentication required'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if not request.user.has_role(Roles.LAUNDRY_STAFF):
            return Response({
                'success': False,
                'error': 'Permission denied: laundry_staff role required'
            }, status=status.HTTP_403_FORBIDDEN)
        
        return view_func(request, *args, **kwargs)
    return wrapper


@api_view(['GET'])
@laundry_staff_api_required
def get_all_laundry_orders(request):
    """Get all laundry orders (Laundry Staff only)"""
    try:
        orders = LaundryOrder.objects.all().order_by('-created_at')
        data = [{
            'id': order.id,
            'invoice_number': order.invoice_number,
            'user_name': order.user.name,
            'user_email': order.user.email,
            'total_amount': float(order.total_amount),
            'total_items': order.total_items,
            'status': order.status,
            'estimated_delivery_date': order.estimated_delivery_date,
            'created_at': order.created_at
        } for order in orders]
        
        return Response({
            'success': True,
            'orders': data,
            'total_count': len(data)
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@laundry_staff_api_required
def update_order_status(request, invoice_number):
    """Update laundry order status (Laundry Staff only)"""
    try:
        new_status = request.data.get('status')
        if not new_status:
            return Response({
                'success': False,
                'error': 'Status is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate status
        valid_statuses = ['processing', 'completed', 'delivered']
        if new_status not in valid_statuses:
            return Response({
                'success': False,
                'error': f'Invalid status. Must be one of: {valid_statuses}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            order = LaundryOrder.objects.get(invoice_number=invoice_number)
        except LaundryOrder.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Order not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        old_status = order.status
        order.status = new_status
        order.save()
        
        return Response({
            'success': True,
            'message': f'Order status updated from {old_status} to {new_status}',
            'order': {
                'invoice_number': order.invoice_number,
                'status': order.status,
                'user_name': order.user.name
            }
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@laundry_staff_api_required
def get_laundry_analytics(request):
    """Get laundry analytics (Laundry Staff only)"""
    try:
        total_orders = LaundryOrder.objects.count()
        processing_orders = LaundryOrder.objects.filter(status='processing').count()
        completed_orders = LaundryOrder.objects.filter(status='completed').count()
        delivered_orders = LaundryOrder.objects.filter(status='delivered').count()
        
        # Calculate total revenue
        from django.db.models import Sum
        total_revenue = LaundryOrder.objects.aggregate(
            total=Sum('total_amount')
        )['total'] or 0
        
        analytics = {
            'total_orders': total_orders,
            'processing_orders': processing_orders,
            'completed_orders': completed_orders,
            'delivered_orders': delivered_orders,
            'total_revenue': float(total_revenue),
            'completion_rate': (delivered_orders / total_orders * 100) if total_orders > 0 else 0
        }
        
        return Response({
            'success': True,
            'analytics': analytics
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@laundry_staff_api_required
def get_order_details_staff(request, invoice_number):
    """Get detailed order information (Laundry Staff only)"""
    try:
        try:
            order = LaundryOrder.objects.get(invoice_number=invoice_number)
        except LaundryOrder.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Order not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        items = order.items.all()
        items_data = [{
            'category': item.category_id,
            'category_name': item.category.name,
            'quantity': item.quantity,
            'wash': item.wash,
            'ironing': item.ironing,
            'subtotal': float(item.subtotal)
        } for item in items]
        
        data = {
            'invoice_number': order.invoice_number,
            'user_name': order.user.name,
            'user_email': order.user.email,
            'user_phone': order.user.phone,
            'total_amount': float(order.total_amount),
            'total_items': order.total_items,
            'status': order.status,
            'estimated_delivery_date': order.estimated_delivery_date,
            'created_at': order.created_at,
            'items': items_data
        }
        
        return Response({
            'success': True,
            'order': data
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
