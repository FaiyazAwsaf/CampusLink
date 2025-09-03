from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import LaundryCategory, LaundryOrder, LaundryOrderItem
from django.utils import timezone
from apps.accounts.decorators import role_required

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

# Staff-only views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@role_required(['laundry_staff'])
def manage_laundry_categories(request):
    """Manage laundry categories - GET all or POST new category"""
    if request.method == 'GET':
        categories = LaundryCategory.objects.all()
        data = [{
            'id': category.id,
            'name': category.name,
            'wash_price': float(category.wash_price),
            'ironing_price': float(category.ironing_price),
            'created_at': category.created_at,
            'updated_at': category.updated_at
        } for category in categories]
        return Response(data)
    
    elif request.method == 'POST':
        try:
            data = request.data
            category = LaundryCategory.objects.create(
                name=data.get('name'),
                wash_price=data.get('wash_price'),
                ironing_price=data.get('ironing_price')
            )
            return Response({
                'id': category.id,
                'name': category.name,
                'wash_price': float(category.wash_price),
                'ironing_price': float(category.ironing_price),
                'created_at': category.created_at,
                'updated_at': category.updated_at
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
@role_required(['laundry_staff'])
def manage_laundry_category(request, category_id):
    """Update or delete a specific laundry category"""
    try:
        category = LaundryCategory.objects.get(id=category_id)
    except LaundryCategory.DoesNotExist:
        return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        try:
            data = request.data
            category.name = data.get('name', category.name)
            category.wash_price = data.get('wash_price', category.wash_price)
            category.ironing_price = data.get('ironing_price', category.ironing_price)
            category.save()
            
            return Response({
                'id': category.id,
                'name': category.name,
                'wash_price': float(category.wash_price),
                'ironing_price': float(category.ironing_price),
                'created_at': category.created_at,
                'updated_at': category.updated_at
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        category.delete()
        return Response({'message': 'Category deleted successfully'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@role_required(['laundry_staff'])
def get_all_orders(request):
    """Get all laundry orders for staff to manage"""
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
    
    return Response(data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@role_required(['laundry_staff'])
def update_order_status(request, order_id):
    """Update order status"""
    try:
        order = LaundryOrder.objects.get(id=order_id)
        new_status = request.data.get('status')
        
        if new_status not in ['processing', 'completed', 'delivered']:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = new_status
        order.save()
        
        return Response({
            'id': order.id,
            'invoice_number': order.invoice_number,
            'status': order.status,
            'updated_at': order.updated_at
        })
    except LaundryOrder.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@role_required(['laundry_staff'])
def get_order_details_staff(request, order_id):
    """Get detailed order information for staff"""
    try:
        order = LaundryOrder.objects.get(id=order_id)
        items = order.items.all()
        
        items_data = [{
            'category_name': item.category.name,
            'quantity': item.quantity,
            'wash': item.wash,
            'ironing': item.ironing,
            'subtotal': float(item.subtotal)
        } for item in items]
        
        data = {
            'id': order.id,
            'invoice_number': order.invoice_number,
            'user_name': order.user.name,
            'user_email': order.user.email,
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

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@role_required(['laundry_staff'])
def delete_order(request, order_id):
    """Delete an order (staff only)"""
    try:
        order = LaundryOrder.objects.get(id=order_id)
        invoice_number = order.invoice_number
        order.delete()
        
        return Response({
            'message': f'Order {invoice_number} has been successfully deleted'
        }, status=status.HTTP_200_OK)
    except LaundryOrder.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
