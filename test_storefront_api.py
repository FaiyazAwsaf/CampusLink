import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from apps.entrepreneurs_hub.models import Storefront
from apps.entrepreneurs_hub.serializers import StorefrontSerializer
from apps.entrepreneurs_hub.views import StorefrontsAPIView
from django.test import RequestFactory

# Test the serializer directly
print("Testing StorefrontSerializer...")
storefronts = Storefront.objects.all()
print(f"Found {storefronts.count()} storefronts")

try:
    serializer = StorefrontSerializer(storefronts, many=True)
    print("Serializer data:", serializer.data)
except Exception as e:
    print("Serializer error:", str(e))
    import traceback
    traceback.print_exc()

# Test the view
print("\nTesting StorefrontsAPIView...")
try:
    rf = RequestFactory()
    request = rf.get('/api/entrepreneurs_hub/products/storefronts/')
    view = StorefrontsAPIView()
    view.setup(request)
    response = view.get(request)
    print('Response status:', response.status_code)
    print('Response data:', response.data)
except Exception as e:
    print('View error:', str(e))
    import traceback
    traceback.print_exc()
