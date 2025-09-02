#!/usr/bin/env python
import os
import sys
import django

# Add the project root directory to the path
sys.path.append('d:/Codes/CampusLink')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from apps.entrepreneurs_hub.models import Storefront, Product

def test_storefront_products():
    """Test if Pias's Store and its products are accessible"""
    
    print("=" * 50)
    print("STOREFRONT & PRODUCT ACCESSIBILITY TEST")
    print("=" * 50)
    
    # Find Pias's Store
    try:
        pias_store = Storefront.objects.get(name="Pias's Store")
        print(f"✅ Found store: {pias_store.name}")
        print(f"   Store ID: {pias_store.store_id}")
        print(f"   Owner: {pias_store.owner.name if pias_store.owner else 'None'}")
        
        # Check products in this store
        products = Product.objects.filter(store_id=pias_store)
        print(f"   Products count: {products.count()}")
        
        for product in products:
            print(f"   - Product: {product.name} (ID: {product.product_id})")
            print(f"     Category: {product.category}")
            print(f"     Price: ${product.price}")
            print(f"     Available: {product.availability}")
        
        # Test API endpoints that the frontend will use
        print(f"\n📡 API Endpoints that should work:")
        print(f"   Public storefront detail: GET /api/entrepreneurs_hub/storefronts/{pias_store.store_id}/")
        print(f"   Public storefront products: GET /api/entrepreneurs_hub/storefronts/{pias_store.store_id}/products/")
        print(f"   Entrepreneur manage: GET /api/entrepreneurs_hub/manage/storefronts/ (auth required)")
        
    except Storefront.DoesNotExist:
        print("❌ Pias's Store not found!")
    
    # Check all products to see if any belong to Pias's Store
    print(f"\n🔍 All products in database:")
    all_products = Product.objects.all()
    for product in all_products:
        store_name = product.store_id.name if product.store_id else "No Store"
        owner_name = product.store_id.owner.name if product.store_id and product.store_id.owner else "No Owner"
        print(f"   - {product.name} → {store_name} (Owner: {owner_name})")

if __name__ == '__main__':
    test_storefront_products()
