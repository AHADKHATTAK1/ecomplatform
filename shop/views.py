from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Product, Category, Order, OrderItem
from decimal import Decimal


def product_list(request):
    """Display all available products"""
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()
    
    # Filter by category if specified
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(name__icontains=search_query)
    
    return render(request, 'shop/product_list.html', {
        'products': products,
        'categories': categories,
        'current_category': category_slug
    })


def product_detail(request, slug):
    """Display product details"""
    product = get_object_or_404(Product, slug=slug, available=True)
    related_products = Product.objects.filter(
        category=product.category,
        available=True
    ).exclude(id=product.id)[:4]
    
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'related_products': related_products
    })


def add_to_cart(request, product_id):
    """Add product to cart"""
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    
    # Add or increment quantity
    product_id_str = str(product_id)
    if product_id_str in cart:
        cart[product_id_str]['quantity'] += 1
    else:
        cart[product_id_str] = {
            'quantity': 1,
            'price': str(product.price),
            'name': product.name
        }
    
    request.session['cart'] = cart
    request.session.modified = True
    messages.success(request, f'{product.name} added to cart!')
    return redirect('product_list')


def view_cart(request):
    """Display shopping cart"""
    cart = request.session.get('cart', {})
    cart_items = []
    total = Decimal('0.00')
    
    for product_id, item_data in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            quantity = item_data['quantity']
            subtotal = product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
            total += subtotal
        except Product.DoesNotExist:
            continue
    
    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total': total
    })


def update_cart(request, product_id):
    """Update cart item quantity"""
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        product_id_str = str(product_id)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            if product_id_str in cart:
                cart[product_id_str]['quantity'] = quantity
                messages.success(request, 'Cart updated!')
        else:
            if product_id_str in cart:
                del cart[product_id_str]
                messages.success(request, 'Item removed from cart!')
        
        request.session['cart'] = cart
        request.session.modified = True
    
    return redirect('view_cart')


def remove_from_cart(request, product_id):
    """Remove item from cart"""
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        del cart[product_id_str]
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, 'Item removed from cart!')
    
    return redirect('view_cart')


@login_required
def checkout(request):
    """Process checkout"""
    cart = request.session.get('cart', {})
    
    if not cart:
        messages.warning(request, 'Your cart is empty!')
        return redirect('product_list')
    
    if request.method == 'POST':
        shipping_address = request.POST.get('shipping_address', '')
        
        if not shipping_address:
            messages.error(request, 'Please provide a shipping address!')
            return render(request, 'shop/checkout.html')
        
        # Calculate total
        total = Decimal('0.00')
        order_items_data = []
        first_product_store = None
        
        for product_id, item_data in cart.items():
            try:
                product = Product.objects.get(id=int(product_id))
                quantity = item_data['quantity']
                
                # Check stock
                if product.stock < quantity:
                    messages.error(request, f'Not enough stock for {product.name}!')
                    return redirect('view_cart')
                
                if first_product_store is None:
                    first_product_store = product.store
                
                subtotal = product.price * quantity
                total += subtotal
                order_items_data.append({
                    'product': product,
                    'quantity': quantity,
                    'price': product.price
                })
            except Product.DoesNotExist:
                continue
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            store=first_product_store,
            total_amount=total,
            shipping_address=shipping_address,
            status='pending'
        )
        
        # Create order items and update stock
        for item_data in order_items_data:
            OrderItem.objects.create(
                order=order,
                product=item_data['product'],
                quantity=item_data['quantity'],
                price=item_data['price']
            )
            item_data['product'].stock -= item_data['quantity']
            item_data['product'].save()
        
        # Clear cart
        request.session['cart'] = {}
        request.session.modified = True
        
        messages.success(request, f'Order #{order.id} placed successfully!')
        return redirect('order_success', order_id=order.id)
    
    # GET request - show checkout form
    cart_items = []
    total = Decimal('0.00')
    
    for product_id, item_data in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            quantity = item_data['quantity']
            subtotal = product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
            total += subtotal
        except Product.DoesNotExist:
            continue
    
    return render(request, 'shop/checkout.html', {
        'cart_items': cart_items,
        'total': total
    })


@login_required
def order_success(request, order_id):
    """Order confirmation page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'shop/order_success.html', {'order': order})


@login_required
def my_orders(request):
    """Display user's orders"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/my_orders.html', {'orders': orders})


def register(request):
    """User registration"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('product_list')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})
