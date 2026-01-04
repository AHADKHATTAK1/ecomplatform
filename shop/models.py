from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse


class Store(models.Model):
    """Multi-tenant store model - each user can create multiple stores"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    description = models.TextField(blank=True)
    domain = models.CharField(max_length=255, blank=True, null=True, unique=True, 
                              help_text="Custom domain (e.g., mystore.com)")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stores')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('store_home', args=[self.slug])


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='categories')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
        unique_together = [['slug', 'store']]  # Unique slug per store

    def __str__(self):
        return f"{self.name} ({self.store.name})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    stock = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = [['slug', 'store']]  # Unique slug per store

    def __str__(self):
        return f"{self.name} ({self.store.name})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('store_product_detail', args=[self.store.slug, self.slug])


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order {self.id} - {self.user.username} ({self.store.name})'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.quantity}x {self.product.name}'

    def get_total(self):
        return self.quantity * self.price


class StoreTheme(models.Model):
    """Store theme customization for visual editor"""
    store = models.OneToOneField(Store, on_delete=models.CASCADE, related_name='theme')
    
    # Theme configuration stored as JSON
    sections = models.JSONField(default=dict, help_text="Page sections configuration")
    
    # Color scheme
    primary_color = models.CharField(max_length=7, default='#007bff')
    secondary_color = models.CharField(max_length=7, default='#6c757d')
    background_color = models.CharField(max_length=7, default='#ffffff')
    text_color = models.CharField(max_length=7, default='#212529')
    
    # Typography
    font_family = models.CharField(max_length=100, default='Arial, sans-serif')
    
    # Logo
    logo = models.ImageField(upload_to='store_logos/', blank=True, null=True)
    
    # Layout settings
    layout_width = models.CharField(max_length=20, default='container', 
                                   choices=[('container', 'Boxed'), ('fluid', 'Full Width')])
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Store Theme'
        verbose_name_plural = 'Store Themes'
    
    def __str__(self):
        return f"Theme for {self.store.name}"
    
    def get_default_sections(self):
        """Returns default sections structure"""
        return {
            'sections': [
                {
                    'id': 'hero',
                    'type': 'hero_banner',
                    'enabled': True,
                    'settings': {
                        'title': f'Welcome to {self.store.name}',
                        'subtitle': 'Discover amazing products',
                        'button_text': 'Shop Now',
                        'background_image': '',
                    }
                },
                {
                    'id': 'featured_products',
                    'type': 'product_grid',
                    'enabled': True,
                    'settings': {
                        'title': 'Featured Products',
                        'products_count': 8,
                    }
                },
                {
                    'id': 'footer',
                    'type': 'footer',
                    'enabled': True,
                    'settings': {
                        'text': f'© 2024 {self.store.name}. All rights reserved.',
                        'social_links': []
                    }
                }
            ]
        }
