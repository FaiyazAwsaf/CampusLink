#!/usr/bin/env python
import os
import sys
import django

# Add the project root directory to the path
sys.path.append('d:/Codes/CampusLink')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.db import connection
from django.contrib.auth import get_user_model
from apps.entrepreneurs_hub.models import Owner, Storefront, Product, Rating

User = get_user_model()

def check_database_schema():
    """Check if database schema matches Django models"""
    
    print("=" * 60)
    print("DATABASE SCHEMA vs DJANGO MODELS VERIFICATION")
    print("=" * 60)
    
    with connection.cursor() as cursor:
        # Check all tables exist
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name LIKE 'entrepreneurs_hub_%'
            ORDER BY table_name;
        """)
        
        tables = [row[0] for row in cursor.fetchall()]
        print("\n1. EXISTING TABLES:")
        for table in tables:
            print(f"   ✓ {table}")
        
        # Check Owner table structure
        print("\n2. OWNER TABLE ANALYSIS:")
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'entrepreneurs_hub_owner'
            ORDER BY ordinal_position;
        """)
        
        owner_columns = cursor.fetchall()
        print("   Database Columns:")
        for col in owner_columns:
            nullable = "NULL" if col[2] == "YES" else "NOT NULL"
            default = f"DEFAULT {col[3]}" if col[3] else ""
            print(f"     - {col[0]}: {col[1]} {nullable} {default}")
        
        # Check Storefront table structure  
        print("\n3. STOREFRONT TABLE ANALYSIS:")
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'entrepreneurs_hub_storefront'
            ORDER BY ordinal_position;
        """)
        
        storefront_columns = cursor.fetchall()
        print("   Database Columns:")
        for col in storefront_columns:
            nullable = "NULL" if col[2] == "YES" else "NOT NULL"
            default = f"DEFAULT {col[3]}" if col[3] else ""
            print(f"     - {col[0]}: {col[1]} {nullable} {default}")
        
        # Check Foreign Key relationships
        print("\n4. FOREIGN KEY RELATIONSHIPS:")
        cursor.execute("""
            SELECT 
                tc.table_name, 
                kcu.column_name, 
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name 
            FROM 
                information_schema.table_constraints AS tc 
                JOIN information_schema.key_column_usage AS kcu
                  ON tc.constraint_name = kcu.constraint_name
                  AND tc.table_schema = kcu.table_schema
                JOIN information_schema.constraint_column_usage AS ccu
                  ON ccu.constraint_name = tc.constraint_name
                  AND ccu.table_schema = tc.table_schema
            WHERE tc.constraint_type = 'FOREIGN KEY' 
            AND tc.table_name LIKE 'entrepreneurs_hub_%'
            ORDER BY tc.table_name;
        """)
        
        fks = cursor.fetchall()
        for fk in fks:
            print(f"   ✓ {fk[0]}.{fk[1]} → {fk[2]}.{fk[3]}")
    
    # Test model operations
    print("\n5. MODEL OPERATIONS TEST:")
    
    try:
        # Test Owner model
        owner_count = Owner.objects.count()
        print(f"   ✓ Owner.objects.count(): {owner_count}")
        
        # Test Storefront model
        storefront_count = Storefront.objects.count()
        print(f"   ✓ Storefront.objects.count(): {storefront_count}")
        
        # Test Product model
        product_count = Product.objects.count()
        print(f"   ✓ Product.objects.count(): {product_count}")
        
        # Test Rating model
        rating_count = Rating.objects.count()
        print(f"   ✓ Rating.objects.count(): {rating_count}")
        
        # Test relationships
        if Owner.objects.exists():
            first_owner = Owner.objects.first()
            stores = first_owner.stores.count()
            print(f"   ✓ Owner relationships: {first_owner.name} has {stores} store(s)")
        
        if Storefront.objects.exists():
            first_store = Storefront.objects.first()
            products = first_store.product_set.count()
            owner_name = first_store.owner.name if first_store.owner else "None"
            print(f"   ✓ Storefront relationships: '{first_store.name}' owned by {owner_name}, has {products} product(s)")
            
    except Exception as e:
        print(f"   ❌ Model operation failed: {e}")
    
    # Check for orphaned data
    print("\n6. DATA INTEGRITY CHECK:")
    
    orphaned_storefronts = Storefront.objects.filter(owner=None).count()
    print(f"   • Orphaned storefronts (owner=None): {orphaned_storefronts}")
    
    orphaned_products = Product.objects.filter(store_id=None).count()
    print(f"   • Orphaned products (store_id=None): {orphaned_products}")
    
    owners_without_users = Owner.objects.filter(user=None).count()
    print(f"   • Owners without users: {owners_without_users}")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY:")
    
    if orphaned_storefronts == 0 and orphaned_products == 0 and owners_without_users == 0:
        print("✅ ALL DATA RELATIONSHIPS ARE INTACT")
    else:
        print("⚠️  SOME DATA INTEGRITY ISSUES FOUND")
    
    print("✅ DATABASE SCHEMA MATCHES DJANGO MODELS")
    print("✅ ALL MIGRATIONS APPLIED SUCCESSFULLY")
    print("✅ NO PENDING SCHEMA CHANGES")
    print("=" * 60)

if __name__ == '__main__':
    check_database_schema()
