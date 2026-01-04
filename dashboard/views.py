from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from shop.models import Product, Category, Order, OrderItem, Store, StoreTheme
import json


@login_required
def store_dashboard(request, store_slug):
    """Store-specific dashboard for store owners"""
    store = get_object_or_404(Store, slug=store_slug, owner=request.user)
    
    # Statistics for this store
    total_orders = Order.objects.filter(store=store).count()
    total_revenue = Order.objects.filter(store=store).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    total_products = Product.objects.filter(store=store).count()
    pending_orders = Order.objects.filter(store=store, status='pending').count()
    
    # Recent orders for this store
    recent_orders = Order.objects.filter(store=store).select_related('user').order_by('-created_at')[:10]
    
    # Low stock products for this store
    low_stock_products = Product.objects.filter(store=store, stock__lt=10).order_by('stock')[:5]
    
    context = {
        'store': store,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_products': total_products,
        'pending_orders': pending_orders,
        'recent_orders': recent_orders,
        'low_stock_products': low_stock_products,
    }
    return render(request, 'dashboard/store_dashboard.html', context)


@login_required
def store_manage_products(request, store_slug):
    """Product management for specific store"""
    store = get_object_or_404(Store, slug=store_slug, owner=request.user)
    products = Product.objects.filter(store=store).select_related('category').order_by('-created_at')
    categories = Category.objects.filter(store=store)
    
    # Search and filter
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )
    
    category_filter = request.GET.get('category')
    if category_filter:
        products = products.filter(category_id=category_filter)
    
    return render(request, 'dashboard/store_products.html', {
        'store': store,
        'products': products,
        'categories': categories
    })


@login_required
def store_add_product(request, store_slug):
    """Add new product to specific store"""
    store = get_object_or_404(Store, slug=store_slug, owner=request.user)
    
    if request.method == 'POST':
        try:
            # Get or create category for this store
            category_id = request.POST.get('category')
            category = get_object_or_404(Category, id=category_id, store=store)
            
            product = Product.objects.create(
                name=request.POST['name'],
                description=request.POST['description'],
                price=request.POST['price'],
                stock=request.POST['stock'],
                category=category,
                store=store,
                available=request.POST.get('available') == 'on'
            )
            
            # Handle image upload
            if 'image' in request.FILES:
                product.image = request.FILES['image']
                product.save()
            
            messages.success(request, 'Product added successfully!')
        except Exception as e:
            messages.error(request, f'Error adding product: {str(e)}')
    
    return redirect('store_manage_products', store_slug=store_slug)


@login_required
def store_add_category(request, store_slug):
    """Add new category to specific store"""
    store = get_object_or_404(Store, slug=store_slug, owner=request.user)
    
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            Category.objects.create(
                name=name,
                store=store
            )
            messages.success(request, f'Category "{name}" added successfully!')
        except Exception as e:
            messages.error(request, f'Error adding category: {str(e)}')
    
    return redirect('store_manage_products', store_slug=store_slug)


@login_required
def store_edit_product(request, store_slug, product_id):
    """Edit product in specific store"""
    store = get_object_or_404(Store, slug=store_slug, owner=request.user)
    product = get_object_or_404(Product, id=product_id, store=store)
    
    if request.method == 'POST':
        try:
            product.name = request.POST['name']
            product.description = request.POST['description']
            product.price = request.POST['price']
            product.stock = request.POST['stock']
            
            category_id = request.POST.get('category')
            if category_id:
                product.category = get_object_or_404(Category, id=category_id, store=store)
            
            product.available = request.POST.get('available') == 'on'
            
            if 'image' in request.FILES:
                product.image = request.FILES['image']
            
            product.save()
            messages.success(request, 'Product updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating product: {str(e)}')
    
    return redirect('store_manage_products', store_slug=store_slug)


@login_required
def store_delete_product(request, store_slug, product_id):
    """Delete product from specific store"""
    store = get_object_or_404(Store, slug=store_slug, owner=request.user)
    product = get_object_or_404(Product, id=product_id, store=store)
    product.delete()
    messages.success(request, 'Product deleted successfully!')
    return redirect('store_manage_products', store_slug=store_slug)


@login_required
def store_manage_orders(request, store_slug):
    """Order management for specific store"""
    store = get_object_or_404(Store, slug=store_slug, owner=request.user)
    orders = Order.objects.filter(store=store).select_related('user').order_by('-created_at')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    return render(request, 'dashboard/store_orders.html', {
        'store': store,
        'orders': orders
    })


@login_required
def store_update_order_status(request, store_slug, order_id):
    """Update order status for specific store"""
    store = get_object_or_404(Store, slug=store_slug, owner=request.user)
    
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id, store=store)
        new_status = request.POST.get('status')
        
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f'Order #{order.id} status updated to {new_status}!')
        else:
            messages.error(request, 'Invalid status!')
    
    return redirect('store_manage_orders', store_slug=store_slug)


@login_required
def store_view_order(request, store_slug, order_id):
    """View order details for specific store"""
    store = get_object_or_404(Store, slug=store_slug, owner=request.user)
    order = get_object_or_404(Order, id=order_id, store=store)
    return render(request, 'dashboard/store_order_detail.html', {
        'store': store,
        'order': order
    })


@login_required
def store_customize(request, store_slug):
    """Theme customization / Visual editor"""
    store = get_object_or_404(Store, slug=store_slug, owner=request.user)
    
    # Get or create theme
    theme, created = StoreTheme.objects.get_or_create(
        store=store,
        defaults={'sections': {}}
    )
    
    # Initialize default sections if empty
    if not theme.sections or theme.sections == {}:
        theme.sections = theme.get_default_sections()
        theme.save()
    
    if request.method == 'POST':
        # Save theme customization
        try:
            theme.primary_color = request.POST.get('primary_color', theme.primary_color)
            theme.secondary_color = request.POST.get('secondary_color', theme.secondary_color)
            theme.background_color = request.POST.get('background_color', theme.background_color)
            theme.text_color = request.POST.get('text_color', theme.text_color)
            theme.font_family = request.POST.get('font_family', theme.font_family)
            theme.layout_width = request.POST.get('layout_width', theme.layout_width)
            
            # Save sections from JSON
            sections_data = request.POST.get('sections_json')
            if sections_data:
                theme.sections = json.loads(sections_data)
            
            # Handle logo upload
            if 'logo' in request.FILES:
                theme.logo = request.FILES['logo']
            
            theme.save()
            messages.success(request, 'Theme updated successfully!')
        except Exception as e:
            messages.error(request, f'Error saving theme: {str(e)}')
    
    return render(request, 'dashboard/store_customize.html', {
        'store': store,
        'theme': theme
    })

