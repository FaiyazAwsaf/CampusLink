from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.laundry.models import LaundryCategory, LaundryOrder, LaundryOrderItem
from datetime import date, timedelta
from decimal import Decimal

User = get_user_model()

class Command(BaseCommand):
    help = 'Create test data for laundry system'

    def handle(self, *args, **options):
        self.stdout.write('Creating test data for laundry system...')

        # Create laundry categories
        categories_data = [
            {'name': 'T-Shirt', 'wash_price': Decimal('25.00'), 'ironing_price': Decimal('15.00')},
            {'name': 'Pants', 'wash_price': Decimal('35.00'), 'ironing_price': Decimal('20.00')},
            {'name': 'Shirt', 'wash_price': Decimal('30.00'), 'ironing_price': Decimal('18.00')},
            {'name': 'Jacket', 'wash_price': Decimal('50.00'), 'ironing_price': Decimal('25.00')},
            {'name': 'Bedsheet', 'wash_price': Decimal('40.00'), 'ironing_price': Decimal('30.00')},
            {'name': 'Pillowcase', 'wash_price': Decimal('15.00'), 'ironing_price': Decimal('10.00')},
        ]

        categories = []
        for cat_data in categories_data:
            category, created = LaundryCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'wash_price': cat_data['wash_price'],
                    'ironing_price': cat_data['ironing_price']
                }
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')
            else:
                self.stdout.write(f'Category already exists: {category.name}')

        # Create test users if they don't exist
        try:
            laundry_staff = User.objects.get(email='laundry@campuslink.com')
            self.stdout.write('Laundry staff user already exists')
        except User.DoesNotExist:
            laundry_staff = User.objects.create_user(
                email='laundry@campuslink.com',
                password='password123',
                name='Laundry Staff',
                role='laundry_staff',
                is_verified=True
            )
            self.stdout.write('Created laundry staff user: laundry@campuslink.com / password123')

        try:
            student = User.objects.get(email='student@campuslink.com')
            self.stdout.write('Student user already exists')
        except User.DoesNotExist:
            student = User.objects.create_user(
                email='student@campuslink.com',
                password='password123',
                name='Test Student',
                role='student',
                is_verified=True
            )
            self.stdout.write('Created student user: student@campuslink.com / password123')

        # Create sample orders
        if LaundryOrder.objects.count() < 5:
            orders_data = [
                {
                    'user': student,
                    'items': [
                        {'category': categories[0], 'quantity': 3, 'wash': True, 'ironing': False},
                        {'category': categories[1], 'quantity': 2, 'wash': True, 'ironing': True},
                    ],
                    'status': 'processing'
                },
                {
                    'user': student,
                    'items': [
                        {'category': categories[2], 'quantity': 1, 'wash': True, 'ironing': True},
                        {'category': categories[4], 'quantity': 2, 'wash': True, 'ironing': False},
                    ],
                    'status': 'completed'
                },
                {
                    'user': student,
                    'items': [
                        {'category': categories[3], 'quantity': 1, 'wash': True, 'ironing': True},
                    ],
                    'status': 'delivered'
                }
            ]

            for order_data in orders_data:
                # Calculate totals
                total_items = sum(item['quantity'] for item in order_data['items'])
                total_amount = Decimal('0.00')
                
                for item in order_data['items']:
                    item_cost = Decimal('0.00')
                    if item['wash']:
                        item_cost += item['category'].wash_price * item['quantity']
                    if item['ironing']:
                        item_cost += item['category'].ironing_price * item['quantity']
                    total_amount += item_cost

                # Create order
                order = LaundryOrder.objects.create(
                    user=order_data['user'],
                    total_amount=total_amount,
                    total_items=total_items,
                    status=order_data['status']
                )

                # Create order items
                for item_data in order_data['items']:
                    item_cost = Decimal('0.00')
                    if item_data['wash']:
                        item_cost += item_data['category'].wash_price * item_data['quantity']
                    if item_data['ironing']:
                        item_cost += item_data['category'].ironing_price * item_data['quantity']

                    LaundryOrderItem.objects.create(
                        order=order,
                        category=item_data['category'],
                        quantity=item_data['quantity'],
                        wash=item_data['wash'],
                        ironing=item_data['ironing'],
                        subtotal=item_cost
                    )

                self.stdout.write(f'Created order: {order.invoice_number}')

        self.stdout.write(self.style.SUCCESS('Test data creation completed!'))
        self.stdout.write('')
        self.stdout.write('You can now test with:')
        self.stdout.write('Laundry Staff: laundry@campuslink.com / password123')
        self.stdout.write('Student: student@campuslink.com / password123')
