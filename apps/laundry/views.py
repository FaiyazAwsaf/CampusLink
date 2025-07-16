from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import LaundryCategory, LaundryOrder, LaundryOrderItem
from django.utils import timezone

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
