from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shop.models import Store, Category, Product
from decimal import Decimal


class Command(BaseCommand):
    help = 'Initialize database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Initializing database...')
        
        # Create admin user if not exists
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('[OK] Admin user created (username: admin, password: admin123)'))
        else:
            self.stdout.write('[OK] Admin user already exists')
        
        # Create default store
        store, created = Store.objects.get_or_create(
            slug='default-store',
            defaults={
                'name': 'ShopPro Store',
                'description': 'Premium e-commerce store with quality products',
                'owner': admin_user,
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'[OK] Created store: {store.name}'))
        
        # Create categories
        categories_data = [
            {'name': 'Electronics', 'slug': 'electronics'},
            {'name': 'Fashion', 'slug': 'fashion'},
            {'name': 'Books', 'slug': 'books'},
            {'name': 'Home & Living', 'slug': 'home-living'},
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                store=store,
                defaults={'name': cat_data['name']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'[OK] Created category: {category.name}'))
        
        # Create products
        electronics = Category.objects.get(slug='electronics', store=store)
        fashion = Category.objects.get(slug='fashion', store=store)
        books = Category.objects.get(slug='books', store=store)
        home = Category.objects.get(slug='home-living', store=store)
        
        products_data = [
            {
                'name': 'Wireless Headphones Pro',
                'slug': 'wireless-headphones-pro',
                'description': 'Premium noise-cancelling wireless headphones with 30-hour battery life. Experience crystal-clear audio and deep bass.',
                'price': Decimal('299.99'),
                'stock': 50,
                'category': electronics,
                'store': store,
            },
            {
                'name': 'Smart Watch Ultra',
                'slug': 'smart-watch-ultra',
                'description': 'Advanced fitness tracking, heart rate monitoring, GPS, and water resistance up to 50m. Stay connected on the go.',
                'price': Decimal('399.99'),
                'stock': 30,
                'category': electronics,
                'store': store,
            },
            {
                'name': '4K Webcam',
                'slug': '4k-webcam',
                'description': 'Professional 4K webcam with auto-focus and noise reduction. Perfect for streaming and video calls.',
                'price': Decimal('149.99'),
                'stock': 45,
                'category': electronics,
                'store': store,
            },
            {
                'name': 'Mechanical Keyboard RGB',
                'slug': 'mechanical-keyboard-rgb',
                'description': 'Gaming mechanical keyboard with customizable RGB lighting and tactile switches.',
                'price': Decimal('129.99'),
                'stock': 60,
                'category': electronics,
                'store': store,
            },
            {
                'name': 'Premium Cotton T-Shirt',
                'slug': 'premium-cotton-tshirt',
                'description': 'Soft, breathable 100% organic cotton t-shirt. Available in multiple colors. Perfect for everyday wear.',
                'price': Decimal('29.99'),
                'stock': 100,
                'category': fashion,
                'store': store,
            },
            {
                'name': 'Designer Sneakers',
                'slug': 'designer-sneakers',
                'description': 'Stylish and comfortable designer sneakers with premium materials and cushioned sole.',
                'price': Decimal('159.99'),
                'stock': 40,
                'category': fashion,
                'store': store,
            },
            {
                'name': 'Leather Jacket',
                'slug': 'leather-jacket',
                'description': 'Genuine leather jacket with classic design. Timeless style that never goes out of fashion.',
                'price': Decimal('399.99'),
                'stock': 20,
                'category': fashion,
                'store': store,
            },
            {
                'name': 'Python Programming Guide',
                'slug': 'python-programming-guide',
                'description': 'Comprehensive guide to Python programming for beginners and advanced developers. 600+ pages.',
                'price': Decimal('49.99'),
                'stock': 75,
                'category': books,
                'store': store,
            },
            {
                'name': 'Web Development Masterclass',
                'slug': 'web-development-masterclass',
                'description': 'Learn modern web development with HTML, CSS, JavaScript, and popular frameworks.',
                'price': Decimal('59.99'),
                'stock': 50,
                'category': books,
                'store': store,
            },
            {
                'name': 'The Art of Design',
                'slug': 'art-of-design',
                'description': 'Beautiful coffee table book featuring stunning design works and creative inspiration.',
                'price': Decimal('79.99'),
                'stock': 30,
                'category': books,
                'store': store,
            },
            {
                'name': 'Minimalist Desk Lamp',
                'slug': 'minimalist-desk-lamp',
                'description': 'Modern LED desk lamp with adjustable brightness and color temperature. Energy efficient.',
                'price': Decimal('89.99'),
                'stock': 55,
                'category': home,
                'store': store,
            },
            {
                'name': 'Ceramic Plant Pot Set',
                'slug': 'ceramic-plant-pot-set',
                'description': 'Set of 3 handcrafted ceramic pots perfect for indoor plants. Modern Scandinavian design.',
                'price': Decimal('39.99'),
                'stock': 80,
                'category': home,
                'store': store,
            },
        ]
        
        for prod_data in products_data:
            product, created = Product.objects.get_or_create(
                slug=prod_data['slug'],
                store=store,
                defaults=prod_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'[OK] Created product: {product.name}'))
        
        self.stdout.write(self.style.SUCCESS('\n=== Database initialization complete! ==='))
        self.stdout.write(self.style.SUCCESS('Admin login: username=admin, password=admin123'))
        self.stdout.write(self.style.SUCCESS('Website: http://127.0.0.1:8000'))
