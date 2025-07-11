from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import LaundryCategory, LaundryInvoice
import json

User = get_user_model()

@require_http_methods(["GET"])
def get_laundry_categories(request):
    """
    Get all active laundry categories with their prices
    """
    try:
        categories = LaundryCategory.objects.filter(active=True).values(
            'id', 'name', 'wash_price', 'iron_price'
        )
        # Convert Decimal to float for JSON serialization
        cat_list = []
        for c in categories:
            cat_list.append({
                "id": c['id'],
                "name": c['name'],
                "wash_price": float(c['wash_price']),
                "iron_price": float(c['iron_price']),
            })
        return JsonResponse({"success": True, "categories": cat_list})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def create_laundry_invoice(request):
    """
    Place a laundry order and generate an invoice (must be authenticated)
    Expects JSON: { items: [{category, quantity, wash, iron}, ...] }
    """
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"success": False, "error": "Authentication required."}, status=401)

        data = json.loads(request.body)
        items = data.get("items", [])
        if not items:
            return JsonResponse({"success": False, "error": "No items provided."}, status=400)

        total_cost = 0
        detailed_items = []
        for item in items:
            cat_name = item["category"]
            qty = int(item["quantity"])
            wash = item.get("wash", False)
            iron = item.get("iron", False)
            try:
                cat_obj = LaundryCategory.objects.get(name=cat_name, active=True)
                wash_price = float(cat_obj.wash_price)
                iron_price = float(cat_obj.iron_price)
            except LaundryCategory.DoesNotExist:
                wash_price = 0
                iron_price = 0

            item_total = 0
            if wash:
                item_total += qty * wash_price
            if iron:
                item_total += qty * iron_price
            detailed_items.append({
                "category": cat_name,
                "quantity": qty,
                "wash": wash,
                "iron": iron,
                "wash_price": wash_price,
                "iron_price": iron_price,
                "item_total": item_total
            })
            total_cost += item_total

        order_date = timezone.now().date()
        delivery_date = order_date + timezone.timedelta(days=3)  # Could make dynamic

        invoice = LaundryInvoice.objects.create(
            user=request.user,
            items_json=detailed_items,
            total_cost=total_cost,
            delivery_date=delivery_date
        )

        resp = {
            "success": True,
            "invoice_id": invoice.id,
            "items": detailed_items,
            "total_cost": total_cost,
            "order_date": str(order_date),
            "delivery_date": str(delivery_date)
        }
        return JsonResponse(resp)
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Invalid JSON data"}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)
